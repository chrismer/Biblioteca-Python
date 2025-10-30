from typing import List, Optional
from datetime import datetime, date, timedelta
from database.db_manager import DBManager, EstanteriaLlenaError
from logic.models import Libro, Estanteria, Usuario, Autor, Genero, Ejemplar, Prestamo

class GestorBiblioteca:
    def __init__(self):
        self.db = DBManager()

    def validar_anio(self, anio: int) -> bool:
        try:
            return 1500 <= anio <= datetime.now().year
        except (ValueError, TypeError):
            return False

    def agregar_estanteria(self, nombre: str, capacidad: int) -> int:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("Nombre debe ser un string no vacío")
        if not isinstance(capacidad, int) or capacidad < 1:
            raise ValueError("Capacidad debe ser un entero positivo")
        
        # Validar que no exista otra estantería con el mismo nombre
        estanterias_existentes = self.db.get_todas_las_estanterias()
        for estanteria in estanterias_existentes:
            if estanteria.nombre.lower().strip() == nombre.lower().strip():
                raise ValueError(f"Ya existe una estantería con el nombre '{nombre}'")
        
        try:
            return self.db.insertar_estanteria(nombre, capacidad)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Ya existe una estantería con el nombre '{nombre}'")
            raise e

    def modificar_estanteria(self, id: int, nombre: Optional[str] = None, capacidad: Optional[int] = None) -> None:
        estanteria = self.db.get_estanteria(id)
        if not estanteria:
            raise ValueError(f"No se encontró estantería con id {id}")
        if nombre is not None:
            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("Nombre debe ser un string no vacío")
            estanteria.nombre = nombre
        if capacidad is not None:
            if not isinstance(capacidad, int) or capacidad < self.db.get_count_libros_en_estanteria(id):
                raise ValueError("Capacidad debe ser >= libros asignados")
            estanteria.capacidad = capacidad
        def _update(cursor):
            cursor.execute("UPDATE estanterias SET nombre = ?, capacidad = ? WHERE id = ?", (estanteria.nombre, estanteria.capacidad, id))
        self.db.execute_transaction(_update)

    def eliminar_estanteria(self, id: int) -> None:
        self.db.eliminar_estanteria(id)
    
    def get_todas_estanterias(self) -> List[Estanteria]:
        """Obtiene todas las estanterías."""
        return self.db.get_todas_las_estanterias()
    
    def get_count_libros_en_estanteria(self, estanteria_id: int) -> int:
        """Obtiene la cantidad de ejemplares en una estantería."""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(e.id) FROM ejemplares e JOIN libros l ON e.libro_id = l.id WHERE l.estanteria_id = ?", (estanteria_id,))
        return cursor.fetchone()[0]

    # ============ ATAJOS DE PRÉSTAMOS (Para GUI) ============
    def prestar_libro(self, codigo: str) -> None:
        """Presta automáticamente el primer ejemplar disponible de un libro.
        
        Esta es una función de conveniencia para la GUI que simplifica
        el préstamo cuando solo se conoce el código del libro.
        """
        libro = self.db.get_libro_por_codigo(codigo)
        if not libro:
            raise ValueError(f"No se encontró libro con código {codigo}")
        
        # Obtener ejemplares de este libro y filtrar los disponibles
        ejemplares = self.get_ejemplares_por_libro(libro.id)
        ejemplares_disponibles = [e for e in ejemplares if e.estado == 'disponible']
        
        if not ejemplares_disponibles:
            raise ValueError("No hay ejemplares disponibles para prestar")
        
        # Prestar el primer ejemplar disponible
        primer_ejemplar = ejemplares_disponibles[0]
        
        # Usar usuario por defecto (ID: 1) para préstamos simples desde GUI
        self.prestar_ejemplar(primer_ejemplar.id, usuario_id=1)

    def devolver_libro(self, codigo: str) -> None:
        """Devuelve automáticamente el primer ejemplar prestado de un libro.
        
        Esta es una función de conveniencia para la GUI que simplifica
        la devolución cuando solo se conoce el código del libro.
        """
        libro = self.db.get_libro_por_codigo(codigo)
        if not libro:
            raise ValueError(f"No se encontró libro con código {codigo}")
        
        # Obtener ejemplares prestados
        ejemplares = self.get_ejemplares_por_libro(libro.id)
        ejemplares_prestados = [e for e in ejemplares if e.estado == 'prestado']
        
        if not ejemplares_prestados:
            raise ValueError("No hay ejemplares prestados para devolver")
        
        # Devolver el primer ejemplar prestado
        primer_prestado = ejemplares_prestados[0]
        self.devolver_ejemplar(primer_prestado.id)

    def buscar_libro_por_codigo(self, codigo: str) -> Optional[Libro]:
        return self.db.get_libro_por_codigo(codigo)

    def buscar_libros_por_titulo(self, titulo: str) -> List[Libro]:
        return self.db.get_libros_por_titulo(titulo)

    def buscar_libros_por_autor(self, autor: str) -> List[Libro]:
        return self.db.get_libros_por_autor(autor)

    def get_libros_disponibles(self) -> List[Libro]:
        return self.db.get_libros_disponibles()

    def get_libros_prestados(self) -> List[Libro]:
        return self.db.get_libros_prestados()

    def get_libro_mas_prestado(self) -> Optional[Libro]:
        return self.db.get_libro_mas_prestado()

    def get_libros_por_estanteria(self, estanteria_id: int) -> List[Libro]:
        return self.db.get_libros_por_estanteria(estanteria_id)

    def cerrar(self):
        self.db.cerrar()

    # ============ GESTIÓN DE USUARIOS ============
    def agregar_usuario(self, nombre: str, email: Optional[str] = None, 
                       telefono: Optional[str] = None, direccion: Optional[str] = None) -> int:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("Nombre debe ser un string no vacío")
        if email and not "@" in email:
            raise ValueError("Email debe tener formato válido")
        return self.db.insertar_usuario(nombre, email, telefono, direccion)

    def get_usuario(self, id: int) -> Optional[Usuario]:
        return self.db.get_usuario(id)

    def get_todos_usuarios(self) -> List[Usuario]:
        return self.db.get_todos_usuarios()

    # ============ GESTIÓN DE AUTORES ============
    def agregar_autor(self, nombre: str, apellido: str, nacionalidad: Optional[str] = None,
                     fecha_nacimiento: Optional[date] = None, biografia: Optional[str] = None) -> int:
        if not all(isinstance(x, str) and x.strip() for x in [nombre, apellido]):
            raise ValueError("Nombre y apellido deben ser strings no vacíos")
        return self.db.insertar_autor(nombre, apellido, nacionalidad, fecha_nacimiento, biografia)

    def get_autor(self, id: int) -> Optional[Autor]:
        return self.db.get_autor(id)

    def get_todos_autores(self) -> List[Autor]:
        return self.db.get_todos_autores()

    # ============ GESTIÓN DE GÉNEROS ============
    def agregar_genero(self, nombre: str, descripcion: Optional[str] = None) -> int:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("Nombre debe ser un string no vacío")
        return self.db.insertar_genero(nombre, descripcion)

    def get_genero(self, id: int) -> Optional[Genero]:
        return self.db.get_genero(id)

    def get_todos_generos(self) -> List[Genero]:
        return self.db.get_todos_generos()

    # ============ GESTIÓN DE EJEMPLARES ============
    def agregar_ejemplar(self, libro_id: int, codigo_ejemplar: str, 
                        ubicacion_fisica: Optional[str] = None, 
                        observaciones: Optional[str] = None) -> int:
        if not isinstance(codigo_ejemplar, str) or not codigo_ejemplar.strip():
            raise ValueError("Código de ejemplar debe ser un string no vacío")
        return self.db.insertar_ejemplar(libro_id, codigo_ejemplar, ubicacion_fisica, observaciones)

    def get_ejemplares_por_libro(self, libro_id: int) -> List[Ejemplar]:
        return self.db.get_ejemplares_por_libro(libro_id)

    def get_ejemplares_disponibles(self) -> List[Ejemplar]:
        return self.db.get_ejemplares_disponibles()

    # ============ SISTEMA DE PRÉSTAMOS NUEVO ============
    def prestar_ejemplar(self, ejemplar_id: int, usuario_id: int, 
                        dias_prestamo: int = 15, observaciones: Optional[str] = None) -> int:
        """Nuevo sistema de préstamos por ejemplar individual."""
        ejemplar = self.db.get_ejemplar(ejemplar_id)
        if not ejemplar:
            raise ValueError(f"No se encontró ejemplar con id {ejemplar_id}")
        if ejemplar.estado != 'disponible':
            raise ValueError(f"Ejemplar no está disponible para préstamo (estado: {ejemplar.estado})")
        
        usuario = self.db.get_usuario(usuario_id)
        if not usuario:
            raise ValueError(f"No se encontró usuario con id {usuario_id}")
        if not usuario.activo:
            raise ValueError("Usuario no está activo")
        
        return self.db.insertar_prestamo(ejemplar_id, usuario_id, dias_prestamo, observaciones)

    def devolver_ejemplar(self, ejemplar_id: int) -> bool:
        """Devuelve un ejemplar específico por su ID."""
        return self.db.devolver_ejemplar_por_id(ejemplar_id)
    
    def devolver_prestamo(self, prestamo_id: int) -> bool:
        """Devuelve un préstamo específico por su ID."""
        return self.db.devolver_prestamo(prestamo_id)

    def get_prestamos_activos(self) -> List[Prestamo]:
        return self.db.get_prestamos_activos()

    def get_prestamos_vencidos(self) -> List[Prestamo]:
        return self.db.get_prestamos_vencidos()

    def get_prestamos_usuario(self, usuario_id: int) -> List[Prestamo]:
        return self.db.get_prestamos_por_usuario(usuario_id)

    # ============ FUNCIONES DE COMPATIBILIDAD  ============
    def agregar_libro_simple(self, codigo: str, titulo: str, autor_nombre: str, autor_apellido: str,
                            anio: int, cantidad_ejemplares: int, estanteria_id: int,
                            genero_nombre: Optional[str] = None, isbn: Optional[str] = None,
                            editorial: Optional[str] = None) -> int:
        """Función simplificada para agregar libro con ejemplares automáticamente."""
        
        # Validaciones básicas
        if not all(isinstance(x, str) and x.strip() for x in [codigo, titulo, autor_nombre, autor_apellido]):
            raise ValueError("Código, título, nombre y apellido del autor deben ser strings no vacíos")
        if not self.validar_anio(anio):
            raise ValueError(f"Año debe estar entre 1500 y {datetime.now().year}")
        if not isinstance(cantidad_ejemplares, int) or cantidad_ejemplares < 1:
            raise ValueError("Cantidad de ejemplares debe ser un entero positivo")
        if not self.db.get_estanteria(estanteria_id):
            raise ValueError(f"Estantería {estanteria_id} no existe")
        
        # Validar que no exista otro libro con el mismo código
        libro_existente = self.db.get_libro_por_codigo(codigo)
        if libro_existente:
            raise ValueError(f"Ya existe un libro con el código '{codigo}'")
        
        # Nota: Los títulos SÍ pueden repetirse según requisitos del proyecto
        
        # Validar capacidad de la estantería
        estanteria = self.db.get_estanteria(estanteria_id)
        if not estanteria:
            raise ValueError(f"Estantería {estanteria_id} no existe")
        
        # Contar ejemplares actuales en la estantería
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(e.id) FROM ejemplares e JOIN libros l ON e.libro_id = l.id WHERE l.estanteria_id = ?", (estanteria_id,))
        ejemplares_actuales = cursor.fetchone()[0]
        
        if (ejemplares_actuales + cantidad_ejemplares) > estanteria.capacidad:
            raise ValueError(f"No hay suficiente espacio en la estantería '{estanteria.nombre}'. "
                           f"Capacidad: {estanteria.capacidad}, Ocupados: {ejemplares_actuales}, "
                           f"Intentando agregar: {cantidad_ejemplares}")

        # Buscar o crear autor
        autores = self.get_todos_autores()
        autor = None
        for a in autores:
            if a.nombre.lower() == autor_nombre.lower() and a.apellido.lower() == autor_apellido.lower():
                autor = a
                break
        
        if not autor:
            autor_id = self.agregar_autor(autor_nombre, autor_apellido)
            autor = self.get_autor(autor_id)

        # Buscar o crear género si se especifica
        genero_id = None
        if genero_nombre:
            generos = self.get_todos_generos()
            genero = None
            for g in generos:
                if g.nombre.lower() == genero_nombre.lower():
                    genero = g
                    break
            
            if not genero:
                genero_id = self.agregar_genero(genero_nombre)
            else:
                genero_id = genero.id

        # Crear libro nuevo
        def _insertar_libro_completo(cursor):
            cursor.execute("""INSERT INTO libros (codigo, titulo, isbn, anio, editorial, autor_id, genero_id, estanteria_id) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                          (codigo, titulo, isbn, anio, editorial, autor.id, genero_id, estanteria_id))
            libro_id = cursor.lastrowid
            
            # Crear ejemplares automáticamente
            for i in range(cantidad_ejemplares):
                codigo_ejemplar = f"{codigo}-{i+1:03d}"
                cursor.execute("""INSERT INTO ejemplares (libro_id, codigo_ejemplar) VALUES (?, ?)""",
                              (libro_id, codigo_ejemplar))
            
            return libro_id
        
        try:
            return self.db.execute_transaction(_insertar_libro_completo)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                if "codigo" in str(e):
                    raise ValueError(f"Ya existe un libro con el código '{codigo}'")
                elif "titulo" in str(e):
                    raise ValueError(f"Ya existe un libro con el título '{titulo}'")
                elif "isbn" in str(e):
                    raise ValueError(f"Ya existe un libro con el ISBN '{isbn}'")
            raise e

    # ============ FUNCIONES DE REPORTES ============
    def get_resumen_biblioteca(self) -> dict:
        """Obtiene un resumen completo de la biblioteca."""
        cursor = self.db.conn.cursor()
        
        # Contar totales
        cursor.execute("SELECT COUNT(*) FROM libros")
        total_libros = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ejemplares")
        total_ejemplares = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ejemplares WHERE estado = 'disponible'")
        ejemplares_disponibles = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM prestamos WHERE estado = 'activo'")
        prestamos_activos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM prestamos WHERE estado = 'activo' AND fecha_devolucion_esperada < CURRENT_DATE")
        prestamos_vencidos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = 1")
        usuarios_activos = cursor.fetchone()[0]
        
        return {
            "total_libros": total_libros,
            "total_ejemplares": total_ejemplares,
            "ejemplares_disponibles": ejemplares_disponibles,
            "ejemplares_prestados": total_ejemplares - ejemplares_disponibles,
            "prestamos_activos": prestamos_activos,
            "prestamos_vencidos": prestamos_vencidos,
            "usuarios_activos": usuarios_activos
        }

    def get_todos_los_libros(self) -> List[Libro]:
        """Obtiene una lista de todos los libros en el sistema."""
        return self.db.get_todos_los_libros()

    def mover_libro(self, libro_id: int, nueva_estanteria_id: int) -> None:
        """Mueve un libro y todos sus ejemplares a una nueva estantería."""
        
        libro = self.db.get_libro_por_id(libro_id)
        if not libro:
            raise ValueError(f"No se encontró el libro con ID {libro_id}")
        
        if libro.estanteria_id == nueva_estanteria_id:
            raise ValueError("El libro ya se encuentra en esa estantería.")

        self.db.mover_libro(libro_id, nueva_estanteria_id)
    
    def buscar_libros(self, termino: str) -> List[Libro]:
        """
        Búsqueda inteligente de libros.
        
        Características:
        - Insensible a mayúsculas/minúsculas  
        - Busca palabras parciales
        - Busca en: título, autor, código, ISBN, editorial
        - Ordena por relevancia (coincidencias exactas primero)
        """
        if not isinstance(termino, str) or not termino.strip():
            return []
        
        # Usar la nueva búsqueda inteligente
        return self.db.buscar_libros_inteligente(termino.strip())
    
    def buscar_libros_por_titulo(self, titulo: str) -> List[Libro]:
        """Búsqueda específica por título (mantiene compatibilidad)."""
        return self.db.get_libros_por_titulo(titulo)
    
    def buscar_libros_por_autor(self, autor: str) -> List[Libro]:
        """Búsqueda específica por autor (mantiene compatibilidad)."""
        return self.db.get_libros_por_autor(autor)

    def eliminar_libro_y_ejemplares(self, libro_id: int) -> None:
        """Elimina un libro y todos sus ejemplares en cascada."""
        # Pre-validación (ej: no se puede borrar si hay préstamos activos)
        ejemplares = self.db.get_ejemplares_por_libro(libro_id)
        for ejemplar in ejemplares:
            if ejemplar.estado == 'prestado':
                raise ValueError(f"No se puede eliminar. El ejemplar {ejemplar.codigo_ejemplar} está prestado.")
        
        self.db.eliminar_libro_por_id(libro_id)

    def modificar_libro_completo(self, libro_id: int, datos_nuevos: dict) -> None:
        """Modifica los datos de un libro."""
        self.db.actualizar_libro_completo(libro_id, datos_nuevos)