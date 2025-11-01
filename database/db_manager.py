import sqlite3
import configparser
from typing import List, Optional, Tuple
from datetime import date, timedelta
from logic.models import Libro, Estanteria, Usuario, Autor, Genero, Ejemplar, Prestamo

class EstanteriaLlenaError(Exception):
    pass

class DBManager:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.conn = sqlite3.connect(config['database']['db_file'])
        self.conn.row_factory = sqlite3.Row

    def execute_transaction(self, func):
        """Ejecuta una función dentro de una transacción y devuelve el resultado."""
        try:
            cursor = self.conn.cursor()
            result = func(cursor)
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            raise e

    def inicializar(self):
        """Inicializa las tablas de la base de datos."""
        self.crear_tablas()

    def crear_tablas(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS estanterias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            capacidad INTEGER NOT NULL
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE,
            telefono TEXT,
            direccion TEXT,
            fecha_registro DATE DEFAULT CURRENT_DATE,
            activo BOOLEAN DEFAULT 1
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS generos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            descripcion TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            nacionalidad TEXT,
            fecha_nacimiento DATE,
            biografia TEXT,
            UNIQUE(nombre, apellido)
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            titulo TEXT NOT NULL,
            isbn TEXT UNIQUE,
            anio INTEGER NOT NULL,
            editorial TEXT,
            numero_paginas INTEGER,
            descripcion TEXT,
            autor_id INTEGER NOT NULL,
            genero_id INTEGER,
            estanteria_id INTEGER NOT NULL,
            fecha_adquisicion DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (autor_id) REFERENCES autores(id),
            FOREIGN KEY (genero_id) REFERENCES generos(id),
            FOREIGN KEY (estanteria_id) REFERENCES estanterias(id)
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS ejemplares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER NOT NULL,
            codigo_ejemplar TEXT UNIQUE NOT NULL,
            estado TEXT DEFAULT 'disponible',
            observaciones TEXT,
            fecha_adquisicion DATE DEFAULT CURRENT_DATE,
            ubicacion_fisica TEXT,
            FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ejemplar_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            fecha_prestamo DATE DEFAULT CURRENT_DATE,
            fecha_devolucion_esperada DATE NOT NULL,
            fecha_devolucion_real DATE NULL,
            estado TEXT DEFAULT 'activo',
            observaciones TEXT,
            renovaciones INTEGER DEFAULT 0,
            FOREIGN KEY (ejemplar_id) REFERENCES ejemplares(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )''')
        self.conn.commit()

    def buscar_libros_inteligente(self, termino: str) -> List[Libro]:
        """
        Búsqueda inteligente que busca en múltiples campos simultáneamente.
        - Insensible a mayúsculas/minúsculas
        - Busca palabras parciales
        - Busca en título, autor completo, código, ISBN
        """
        if not termino or not termino.strip():
            return []
        
        cursor = self.conn.cursor()
        # Búsqueda unificada en todos los campos relevantes
        cursor.execute("""
            SELECT DISTINCT l.*, 
                   a.nombre as autor_nombre, a.apellido as autor_apellido,
                   g.nombre as genero_nombre
            FROM libros l
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN generos g ON l.genero_id = g.id
            WHERE LOWER(l.titulo) LIKE LOWER(?)
               OR LOWER(l.codigo) LIKE LOWER(?)
               OR LOWER(l.isbn) LIKE LOWER(?)
               OR LOWER(a.nombre) LIKE LOWER(?)
               OR LOWER(a.apellido) LIKE LOWER(?)
               OR LOWER(a.nombre || ' ' || a.apellido) LIKE LOWER(?)
               OR LOWER(l.editorial) LIKE LOWER(?)
            ORDER BY 
                -- Priorizar coincidencias exactas
                CASE WHEN LOWER(l.titulo) = LOWER(?) THEN 1
                     WHEN LOWER(l.codigo) = LOWER(?) THEN 2
                     WHEN LOWER(a.nombre || ' ' || a.apellido) = LOWER(?) THEN 3
                     ELSE 4 END,
                l.titulo
        """, (f"%{termino}%", f"%{termino}%", f"%{termino}%", f"%{termino}%", 
              f"%{termino}%", f"%{termino}%", f"%{termino}%",
              termino, termino, termino))
        return [self._hidratar_libro(row) for row in cursor.fetchall()]

    def insertar_libro(self, libro: Libro) -> int:
        def _insert(cursor):
            cursor.execute("SELECT COUNT(*) FROM libros WHERE estanteria_id = ?", (libro.estanteria_id,))
            count = cursor.fetchone()[0]
            cursor.execute("SELECT capacidad FROM estanterias WHERE id = ?", (libro.estanteria_id,))
            capacidad = cursor.fetchone()[0]
            if count >= capacidad:
                raise EstanteriaLlenaError(f"Estantería {libro.estanteria_id} llena.")
            cursor.execute('''INSERT INTO libros (codigo, titulo, autor, anio, cantidad_total, cantidad_prestados, historial_prestamos, estanteria_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                          (libro.codigo, libro.titulo, libro.autor, libro.anio, libro.cantidad_total, libro.cantidad_prestados, libro.historial_prestamos, libro.estanteria_id))
            return cursor.lastrowid
        return self.execute_transaction(_insert)

    def insertar_estanteria(self, nombre: str, capacidad: int) -> int:
        """Inserta una nueva estantería en la base de datos."""
        def _insert(cursor):
            cursor.execute("INSERT INTO estanterias (nombre, capacidad) VALUES (?, ?)", 
                         (nombre, capacidad))
            return cursor.lastrowid
        return self.execute_transaction(_insert)

    def eliminar_estanteria(self, id: int):
        def _delete(cursor):
            cursor.execute("SELECT COUNT(*) FROM libros WHERE estanteria_id = ?", (id,))
            if cursor.fetchone()[0] > 0:
                raise ValueError("No se puede eliminar estantería con libros asignados")
            cursor.execute("DELETE FROM estanterias WHERE id = ?", (id,))
            if cursor.rowcount == 0:
                raise ValueError(f"No se encontró estantería con id {id}")
        self.execute_transaction(_delete)

    def get_libro_por_codigo(self, codigo: str) -> Optional[Libro]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE codigo = ?", (codigo,))
        row = cursor.fetchone()
        if row:
            # Verificar si es modelo anterior o nuevo
            # Usar la función de compatibilidad unificada
            return self._hidratar_libro(row)
        return None

    def get_estanteria(self, id: int) -> Optional[Estanteria]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM estanterias WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Estanteria(row['id'], row['nombre'], row['capacidad'])
        return None

    def get_count_libros_en_estanteria(self, estanteria_id: int) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros WHERE estanteria_id = ?", (estanteria_id,))
        return cursor.fetchone()[0]

    def get_libros_por_estanteria(self, estanteria_id: int) -> List[Libro]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE estanteria_id = ?", (estanteria_id,))
        return [self._hidratar_libro(row) for row in cursor.fetchall()]

    def get_libros_disponibles(self) -> List[Libro]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT l.*, 
                   a.nombre as autor_nombre, a.apellido as autor_apellido,
                   g.nombre as genero_nombre
            FROM libros l
            JOIN ejemplares e ON l.id = e.libro_id
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN generos g ON l.genero_id = g.id
            WHERE e.estado = 'disponible'
            GROUP BY l.id, a.id, g.id
        """)
        return [self._hidratar_libro(row) for row in cursor.fetchall()]

    def get_libros_prestados(self) -> List[Libro]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT l.*, 
                   a.nombre as autor_nombre, a.apellido as autor_apellido,
                   g.nombre as genero_nombre
            FROM libros l
            JOIN ejemplares e ON l.id = e.libro_id
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN generos g ON l.genero_id = g.id
            WHERE e.estado = 'prestado'
            GROUP BY l.id, a.id, g.id
        """)
        return [self._hidratar_libro(row) for row in cursor.fetchall()]

    def get_libro_mas_prestado(self) -> Optional[Libro]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT l.*, COUNT(p.id) as total_prestamos,
                   a.nombre as autor_nombre, a.apellido as autor_apellido,
                   g.nombre as genero_nombre
            FROM libros l
            LEFT JOIN ejemplares e ON l.id = e.libro_id
            LEFT JOIN prestamos p ON e.id = p.ejemplar_id
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN generos g ON l.genero_id = g.id
            GROUP BY l.id, a.id, g.id
            ORDER BY total_prestamos DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row and row['total_prestamos'] > 0:
            return self._hidratar_libro(row)
        return None

    def get_todas_las_estanterias(self) -> List[Estanteria]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM estanterias ORDER BY nombre")
        return [Estanteria(row['id'], row['nombre'], row['capacidad']) for row in cursor.fetchall()]

    def cerrar(self):
        self.conn.close()

    # ============ FUNCIÓN DE HIDRATACIÓN ============
    def _hidratar_libro(self, row) -> 'Libro':
        """Convierte una fila de base de datos en un objeto Libro completo.
        
        Hidrata el libro con todas sus relaciones:
        - Autor (objeto Autor completo)
        - Género (objeto Genero completo)
        - Ejemplares (lista de objetos Ejemplar)
        - Historial de préstamos (si está disponible en la consulta)
        
        Args:
            row: Fila de sqlite3 (sqlite3.Row o dict) con datos del libro
            
        Returns:
            Libro: Objeto Libro completamente hidratado con todas sus relaciones
        """
        from logic.models import Libro
        
        # Convertir sqlite3.Row a dict si es necesario
        if hasattr(row, 'keys'):
            row_dict = dict(row)
        else:
            row_dict = row
        
        # Crear libro con todos sus campos
        libro = Libro(
            id=row_dict['id'],
            codigo=row_dict['codigo'],
            titulo=row_dict['titulo'],
            isbn=row_dict.get('isbn'),
            anio=row_dict['anio'],
            editorial=row_dict.get('editorial'),
            numero_paginas=row_dict.get('numero_paginas'),
            descripcion=row_dict.get('descripcion'),
            autor_id=row_dict['autor_id'],
            genero_id=row_dict.get('genero_id'),
            estanteria_id=row_dict['estanteria_id'],
            fecha_adquisicion=row_dict.get('fecha_adquisicion')
        )
        
        # Poblar datos relacionados
        try:
            # Poblar autor - usar datos de la consulta si están disponibles
            if 'autor_nombre' in row_dict and 'autor_apellido' in row_dict:
                from logic.models import Autor
                libro.autor = Autor(
                    id=libro.autor_id,
                    nombre=row_dict['autor_nombre'],
                    apellido=row_dict['autor_apellido']
                )
            elif libro.autor_id:
                libro.autor = self.get_autor(libro.autor_id)
            
            # Poblar género - usar datos de la consulta si están disponibles
            if 'genero_nombre' in row_dict and row_dict['genero_nombre']:
                from logic.models import Genero
                libro.genero = Genero(
                    id=libro.genero_id,
                    nombre=row_dict['genero_nombre']
                )
            elif libro.genero_id:
                libro.genero = self.get_genero(libro.genero_id)
            
            # Poblar ejemplares - siempre necesario para calcular disponibles/prestados
            if libro.id:
                libro.ejemplares = self.get_ejemplares_por_libro(libro.id)
            
            # Poblar historial de préstamos si está en la consulta
            if 'total_prestamos' in row_dict:
                libro.historial_prestamos = row_dict['total_prestamos']
                
        except Exception as e:
            print(f"⚠️ Error poblando datos relacionados para libro {libro.codigo}: {e}")
            # Continúa con libro básico si hay error
        
        return libro

    # ============ FUNCIONES PARA USUARIOS ============
    def insertar_usuario(self, nombre: str, email: Optional[str] = None, 
                        telefono: Optional[str] = None, direccion: Optional[str] = None) -> int:
        def _insert(cursor):
            cursor.execute("""INSERT INTO usuarios (nombre, email, telefono, direccion) 
                            VALUES (?, ?, ?, ?)""", (nombre, email, telefono, direccion))
            return cursor.lastrowid
        return self.execute_transaction(_insert)

    def get_usuario(self, id: int) -> Optional[Usuario]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Usuario(row['id'], row['nombre'], row['email'], row['telefono'], 
                         row['direccion'], row['fecha_registro'], row['activo'])
        return None

    def get_todos_usuarios(self) -> List[Usuario]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE activo = 1 ORDER BY nombre")
        return [Usuario(row['id'], row['nombre'], row['email'], row['telefono'], 
                       row['direccion'], row['fecha_registro'], row['activo']) 
                for row in cursor.fetchall()]

    # ============ FUNCIONES PARA AUTORES ============
    def insertar_autor(self, nombre: str, apellido: str, nacionalidad: Optional[str] = None,
                      fecha_nacimiento: Optional[date] = None, biografia: Optional[str] = None) -> int:
        def _insert(cursor):
            cursor.execute("""INSERT INTO autores (nombre, apellido, nacionalidad, fecha_nacimiento, biografia) 
                            VALUES (?, ?, ?, ?, ?)""", 
                          (nombre, apellido, nacionalidad, fecha_nacimiento, biografia))
            return cursor.lastrowid
        return self.execute_transaction(_insert)

    def get_autor(self, id: int) -> Optional[Autor]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM autores WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Autor(row['id'], row['nombre'], row['apellido'], row['nacionalidad'], 
                        row['fecha_nacimiento'], row['biografia'])
        return None

    def get_todos_autores(self) -> List[Autor]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM autores ORDER BY apellido, nombre")
        return [Autor(row['id'], row['nombre'], row['apellido'], row['nacionalidad'], 
                     row['fecha_nacimiento'], row['biografia']) 
                for row in cursor.fetchall()]

    # ============ FUNCIONES PARA GÉNEROS ============
    def insertar_genero(self, nombre: str, descripcion: Optional[str] = None) -> int:
        def _insert(cursor):
            cursor.execute("INSERT INTO generos (nombre, descripcion) VALUES (?, ?)", 
                          (nombre, descripcion))
            return cursor.lastrowid
        return self.execute_transaction(_insert)

    def get_genero(self, id: int) -> Optional[Genero]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM generos WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Genero(row['id'], row['nombre'], row['descripcion'])
        return None

    def get_todos_generos(self) -> List[Genero]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM generos ORDER BY nombre")
        return [Genero(row['id'], row['nombre'], row['descripcion']) 
                for row in cursor.fetchall()]

    # ============ FUNCIONES PARA EJEMPLARES ============
    def _generar_ubicacion_automatica(self, libro_id: int) -> str:
        """Genera una ubicación automática para un ejemplar basada en la estantería del libro."""
        cursor = self.conn.cursor()
        
        # Obtener información del libro y estantería
        cursor.execute("""
            SELECT l.estanteria_id, e.nombre as estanteria_nombre
            FROM libros l
            JOIN estanterias e ON l.estanteria_id = e.id
            WHERE l.id = ?
        """, (libro_id,))
        
        libro_info = cursor.fetchone()
        if not libro_info:
            return "Ubicación no especificada"
        
        estanteria_nombre = libro_info['estanteria_nombre']
        
        # Contar ejemplares existentes en la misma estantería para generar posición
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM ejemplares ej
            JOIN libros l ON ej.libro_id = l.id
            WHERE l.estanteria_id = ?
        """, (libro_info['estanteria_id'],))
        
        total_ejemplares = cursor.fetchone()['total'] + 1  # +1 para el nuevo ejemplar
        
        # Calcular nivel y posición (10 libros por nivel)
        nivel = ((total_ejemplares - 1) // 10) + 1
        posicion = ((total_ejemplares - 1) % 10) + 1
        
        return f"Estantería {estanteria_nombre} - Nivel {nivel} - Pos {posicion}"

    def insertar_ejemplar(self, libro_id: int, codigo_ejemplar: str, 
                         ubicacion_fisica: Optional[str] = None, 
                         observaciones: Optional[str] = None) -> int:
        def _insert(cursor):
            # Si no se especifica ubicación, generar una automática
            if ubicacion_fisica is None:
                ubicacion_auto = self._generar_ubicacion_automatica(libro_id)
            else:
                ubicacion_auto = ubicacion_fisica
                
            cursor.execute("""INSERT INTO ejemplares (libro_id, codigo_ejemplar, ubicacion_fisica, observaciones) 
                            VALUES (?, ?, ?, ?)""", 
                          (libro_id, codigo_ejemplar, ubicacion_auto, observaciones))
            return cursor.lastrowid
        return self.execute_transaction(_insert)

    def get_ejemplar(self, id: int) -> Optional[Ejemplar]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM ejemplares WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Ejemplar(row['id'], row['libro_id'], row['codigo_ejemplar'], 
                          row['estado'], row['observaciones'], row['fecha_adquisicion'], 
                          row['ubicacion_fisica'])
        return None

    def get_ejemplares_por_libro(self, libro_id: int) -> List[Ejemplar]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM ejemplares WHERE libro_id = ? ORDER BY codigo_ejemplar", 
                      (libro_id,))
        return [Ejemplar(row['id'], row['libro_id'], row['codigo_ejemplar'], 
                        row['estado'], row['observaciones'], row['fecha_adquisicion'], 
                        row['ubicacion_fisica']) for row in cursor.fetchall()]

    def get_ejemplares_disponibles(self) -> List[Ejemplar]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM ejemplares WHERE estado = 'disponible' ORDER BY codigo_ejemplar")
        return [Ejemplar(row['id'], row['libro_id'], row['codigo_ejemplar'], 
                        row['estado'], row['observaciones'], row['fecha_adquisicion'], 
                        row['ubicacion_fisica']) for row in cursor.fetchall()]

    # ============ FUNCIONES PARA PRÉSTAMOS ============
    def insertar_prestamo(self, ejemplar_id: int, usuario_id: int, 
                         dias_prestamo: int = 15, observaciones: Optional[str] = None) -> int:
        def _insert(cursor):
            fecha_devolucion = date.today() + timedelta(days=dias_prestamo)
            cursor.execute("""INSERT INTO prestamos (ejemplar_id, usuario_id, fecha_devolucion_esperada, observaciones) 
                            VALUES (?, ?, ?, ?)""", 
                          (ejemplar_id, usuario_id, fecha_devolucion, observaciones))
            # Actualizar estado del ejemplar
            cursor.execute("UPDATE ejemplares SET estado = 'prestado' WHERE id = ?", (ejemplar_id,))
            return cursor.lastrowid
        return self.execute_transaction(_insert)

    def devolver_prestamo(self, prestamo_id: int) -> bool:
        def _devolver(cursor):
            # Obtener información del préstamo
            cursor.execute("SELECT ejemplar_id FROM prestamos WHERE id = ? AND estado = 'activo'", 
                          (prestamo_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"No se encontró préstamo activo con id {prestamo_id}")
            
            ejemplar_id = row['ejemplar_id']
            
            # Actualizar préstamo
            cursor.execute("""UPDATE prestamos SET estado = 'devuelto', fecha_devolucion_real = CURRENT_DATE 
                            WHERE id = ?""", (prestamo_id,))
            
            # Actualizar ejemplar
            cursor.execute("UPDATE ejemplares SET estado = 'disponible' WHERE id = ?", (ejemplar_id,))
            return True
        return self.execute_transaction(_devolver)
    
    def devolver_ejemplar_por_id(self, ejemplar_id: int) -> bool:
        """Devuelve un ejemplar específico por su ID, buscando automáticamente el préstamo activo."""
        def _devolver(cursor):
            # Buscar préstamo activo para este ejemplar
            cursor.execute("SELECT id FROM prestamos WHERE ejemplar_id = ? AND estado = 'activo'", 
                          (ejemplar_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"No se encontró préstamo activo para el ejemplar con id {ejemplar_id}")
            
            prestamo_id = row['id']
            
            # Actualizar préstamo
            cursor.execute("""UPDATE prestamos SET estado = 'devuelto', fecha_devolucion_real = CURRENT_DATE 
                            WHERE id = ?""", (prestamo_id,))
            
            # Actualizar ejemplar
            cursor.execute("UPDATE ejemplares SET estado = 'disponible' WHERE id = ?", (ejemplar_id,))
            return True
        return self.execute_transaction(_devolver)

    def get_prestamo(self, id: int) -> Optional[Prestamo]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM prestamos WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return self._crear_prestamo_from_row(row)
        return None

    def get_prestamos_activos(self) -> List[Prestamo]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM prestamos WHERE estado = 'activo' ORDER BY fecha_prestamo")
        return [self._crear_prestamo_from_row(row) for row in cursor.fetchall()]
    
    def _crear_prestamo_from_row(self, row) -> 'Prestamo':
        """Crea un objeto Prestamo desde una fila de base de datos, convirtiendo fechas correctamente."""
        from logic.models import Prestamo
        from datetime import datetime, date
        
        def parse_date(date_str):
            """Convierte string de fecha a objeto date."""
            if date_str is None:
                return None
            if isinstance(date_str, date):
                return date_str
            if isinstance(date_str, str):
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    return None
            return None
        
        return Prestamo(
            id=row['id'],
            ejemplar_id=row['ejemplar_id'],
            usuario_id=row['usuario_id'],
            fecha_prestamo=parse_date(row['fecha_prestamo']),
            fecha_devolucion_esperada=parse_date(row['fecha_devolucion_esperada']),
            fecha_devolucion_real=parse_date(row['fecha_devolucion_real']),
            estado=row['estado'],
            observaciones=row['observaciones'],
            renovaciones=row['renovaciones'] or 0
        )

    def get_prestamos_vencidos(self) -> List[Prestamo]:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM prestamos 
                         WHERE estado = 'activo' AND fecha_devolucion_esperada < CURRENT_DATE 
                         ORDER BY fecha_devolucion_esperada""")
        return [self._crear_prestamo_from_row(row) for row in cursor.fetchall()]

    def get_prestamos_por_usuario(self, usuario_id: int) -> List[Prestamo]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM prestamos WHERE usuario_id = ? ORDER BY fecha_prestamo DESC", 
                      (usuario_id,))
        return [self._crear_prestamo_from_row(row) for row in cursor.fetchall()]


    def get_libro_por_id(self, libro_id: int) -> Optional[Libro]:
        """Obtiene un libro por su ID con datos relacionados."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT l.*, 
                   a.nombre as autor_nombre, a.apellido as autor_apellido,
                   g.nombre as genero_nombre
            FROM libros l
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN generos g ON l.genero_id = g.id
            WHERE l.id = ?
        """, (libro_id,))
        row = cursor.fetchone()
        if row:
            return self._hidratar_libro(row)
        return None

    def get_todos_los_libros(self) -> List[Libro]:
        """Obtiene todos los libros de la base de datos con datos relacionados."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT l.*, 
                   a.nombre as autor_nombre, a.apellido as autor_apellido,
                   g.nombre as genero_nombre
            FROM libros l
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN generos g ON l.genero_id = g.id
            ORDER BY l.titulo
        """)
        return [self._hidratar_libro(row) for row in cursor.fetchall()]

    # función mover_libro para que chequee la cantidad de ejemplares
    def mover_libro(self, libro_id: int, nueva_estanteria_id: int):
        def _mover(cursor):
            
            cursor.execute("SELECT COUNT(e.id) FROM ejemplares e JOIN libros l ON e.libro_id = l.id WHERE l.estanteria_id = ?", (nueva_estanteria_id,))
            count = cursor.fetchone()[0]
            
            cursor.execute("SELECT capacidad, nombre FROM estanterias WHERE id = ?", (nueva_estanteria_id,))
            row_estanteria = cursor.fetchone()
            if not row_estanteria:
                raise ValueError(f"Estantería {nueva_estanteria_id} no existe")
            capacidad = row_estanteria['capacidad']
            nueva_estanteria_nombre = row_estanteria['nombre']
            
            cursor.execute("SELECT COUNT(*) FROM ejemplares WHERE libro_id = ?", (libro_id,))
            ejemplares_a_mover = cursor.fetchone()[0]
            
            espacios_libres = capacidad - count

            if ejemplares_a_mover > espacios_libres:
                raise EstanteriaLlenaError(
                    f"No hay suficiente espacio en la estantería '{nueva_estanteria_nombre}'.\n\n"
                    f"📦 Ejemplares a mover: {ejemplares_a_mover}\n"
                    f"📊 Capacidad total: {capacidad}\n"
                    f"🔢 Ejemplares actuales: {count}\n"
                    f"✅ Espacios libres: {espacios_libres}\n\n"
                    f"Necesitas una estantería con al menos {ejemplares_a_mover} espacios libres."
                )
            
            
            cursor.execute("UPDATE libros SET estanteria_id = ? WHERE id = ?", (nueva_estanteria_id, libro_id))
            if cursor.rowcount == 0:
                raise ValueError(f"No se encontró libro con id {libro_id}")


            # Obtenemos todos los ejemplares del libro que se movió
            cursor.execute("SELECT id, codigo_ejemplar FROM ejemplares WHERE libro_id = ? ORDER BY codigo_ejemplar", (libro_id,))
            ejemplares = cursor.fetchall()
            
            # Re-calculamos y actualizamos la ubicación para cada uno
            for i, ejemplar in enumerate(ejemplares, 1):
                nivel = ((i - 1) // 10) + 1
                posicion = ((i - 1) % 10) + 1
                
                nueva_ubicacion = f"Estantería {nueva_estanteria_nombre} - Nivel {nivel} - Pos {posicion}"
                
                cursor.execute("UPDATE ejemplares SET ubicacion_fisica = ? WHERE id = ?", (nueva_ubicacion, ejemplar['id']))

        self.execute_transaction(_mover)
    
    def eliminar_libro_por_id(self, libro_id: int):
        def _delete(cursor):
            cursor.execute("DELETE FROM libros WHERE id = ?", (libro_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"No se encontró libro con id {libro_id}")
        self.execute_transaction(_delete)
    
    def modificar_libro_completo(self, libro_id: int, cambios: dict) -> bool:
        """Modifica un libro completamente incluyendo autor, género y estantería."""
        try:
            def transaction(cursor):
                
                # 1. Verificar/crear autor
                autor_id = None
                if 'autor_nombre' in cambios and 'autor_apellido' in cambios:
                    cursor.execute("""
                        SELECT id FROM autores 
                        WHERE LOWER(nombre) = LOWER(?) AND LOWER(apellido) = LOWER(?)
                    """, (cambios['autor_nombre'], cambios['autor_apellido']))
                    
                    autor_row = cursor.fetchone()
                    if autor_row:
                        autor_id = autor_row[0]
                    else:
                        # Crear nuevo autor
                        cursor.execute("""
                            INSERT INTO autores (nombre, apellido)
                            VALUES (?, ?)
                        """, (cambios['autor_nombre'], cambios['autor_apellido']))
                        autor_id = cursor.lastrowid
                
                # 2. Verificar/crear género
                genero_id = None
                if cambios.get('genero'):
                    cursor.execute("""
                        SELECT id FROM generos WHERE LOWER(nombre) = LOWER(?)
                    """, (cambios['genero'],))
                    
                    genero_row = cursor.fetchone()
                    if genero_row:
                        genero_id = genero_row[0]
                    else:
                        # Crear nuevo género
                        cursor.execute("""
                            INSERT INTO generos (nombre) VALUES (?)
                        """, (cambios['genero'],))
                        genero_id = cursor.lastrowid
                
                # 3. Actualizar libro
                update_fields = []
                update_values = []
                
                if 'titulo' in cambios:
                    update_fields.append("titulo = ?")
                    update_values.append(cambios['titulo'])
                    
                if 'isbn' in cambios:
                    update_fields.append("isbn = ?")
                    update_values.append(cambios['isbn'])
                    
                if 'anio' in cambios:
                    update_fields.append("anio = ?")
                    update_values.append(cambios['anio'])
                    
                if 'editorial' in cambios:
                    update_fields.append("editorial = ?")
                    update_values.append(cambios['editorial'])
                    
                if 'numero_paginas' in cambios:
                    update_fields.append("numero_paginas = ?")
                    update_values.append(cambios['numero_paginas'])
                    
                if 'descripcion' in cambios:
                    update_fields.append("descripcion = ?")
                    update_values.append(cambios['descripcion'])
                    
                if autor_id:
                    update_fields.append("autor_id = ?")
                    update_values.append(autor_id)
                    
                if genero_id:
                    update_fields.append("genero_id = ?")
                    update_values.append(genero_id)
                    
                if 'estanteria_id' in cambios:
                    update_fields.append("estanteria_id = ?")
                    update_values.append(cambios['estanteria_id'])
                
                # Ejecutar actualización
                if update_fields:
                    update_values.append(libro_id)
                    cursor.execute(f"""
                        UPDATE libros 
                        SET {', '.join(update_fields)}
                        WHERE id = ?
                    """, update_values)
                
                # 4. Si cambió la estantería, actualizar ubicaciones de ejemplares
                if 'estanteria_id' in cambios:
                    # Obtener nombre de la nueva estantería
                    cursor.execute("SELECT nombre FROM estanterias WHERE id = ?", (cambios['estanteria_id'],))
                    estanteria_row = cursor.fetchone()
                    nueva_estanteria_nombre = estanteria_row['nombre'] if estanteria_row else f"ID-{cambios['estanteria_id']}"
                    
                    # Obtener ejemplares del libro
                    cursor.execute("SELECT id, codigo_ejemplar FROM ejemplares WHERE libro_id = ? ORDER BY codigo_ejemplar", (libro_id,))
                    ejemplares = cursor.fetchall()
                    
                    # Actualizar ubicación de cada ejemplar
                    for i, ejemplar in enumerate(ejemplares, 1):
                        nivel = ((i - 1) // 10) + 1
                        posicion = ((i - 1) % 10) + 1
                        nueva_ubicacion = f"Estantería {nueva_estanteria_nombre} - Nivel {nivel} - Pos {posicion}"
                        
                        cursor.execute("""
                            UPDATE ejemplares 
                            SET ubicacion_fisica = ?
                            WHERE id = ?
                        """, (nueva_ubicacion, ejemplar['id']))
                
                return True
            
            return self.execute_transaction(transaction)
            
        except Exception as e:
            print(f"Error modificando libro: {e}")
            return False
