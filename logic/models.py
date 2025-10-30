from typing import Optional, List
import datetime
from datetime import date

class Estanteria:
    def __init__(self, id: int, nombre: str, capacidad: int):
        self.id = id
        self.nombre = nombre
        self.capacidad = int(capacidad)

    def get_libros_asignados(self, gestor: 'GestorBiblioteca') -> list['Libro']:
        """Consulta libros asignados a esta estantería via gestor."""
        return gestor.get_libros_por_estanteria(self.id)

class Usuario:
    def __init__(self, id: int, nombre: str, email: Optional[str] = None, 
                 telefono: Optional[str] = None, direccion: Optional[str] = None,
                 fecha_registro: Optional[date] = None, activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.fecha_registro = fecha_registro or date.today()
        self.activo = activo

class Genero:
    def __init__(self, id: int, nombre: str, descripcion: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

class Autor:
    def __init__(self, id: int, nombre: str, apellido: str, 
                 nacionalidad: Optional[str] = None, fecha_nacimiento: Optional[date] = None,
                 biografia: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.biografia = biografia
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

class Libro:
    def __init__(self, id: int, codigo: str, titulo: str, isbn: Optional[str] = None,
                 anio: int = 0, editorial: Optional[str] = None, numero_paginas: Optional[int] = None,
                 descripcion: Optional[str] = None, autor_id: int = 0, genero_id: Optional[int] = None,
                 estanteria_id: int = 0, fecha_adquisicion: Optional[date] = None):
        self.id = id
        self.codigo = codigo
        self.titulo = titulo
        self.isbn = isbn
        self.anio = int(anio)
        self.editorial = editorial
        self.numero_paginas = numero_paginas
        self.descripcion = descripcion
        self.autor_id = autor_id
        self.genero_id = genero_id
        self.estanteria_id = estanteria_id
        self.fecha_adquisicion = fecha_adquisicion or date.today()
        
        # Atributos para guardar los objetos relacionados "hidratados"
        self.autor: Optional[Autor] = None
        self.genero: Optional[Genero] = None
        self.ejemplares: List[Ejemplar] = []
        self.historial_prestamos: int = 0 

    @property
    def cantidad_disponibles(self) -> int:
        return len([e for e in self.ejemplares if e.estado == 'disponible'])
    
    @property
    def cantidad_prestados(self) -> int:
        return len([e for e in self.ejemplares if e.estado == 'prestado'])

class Ejemplar:
    def __init__(self, id: int, libro_id: int, codigo_ejemplar: str,
                 estado: str = 'disponible', observaciones: Optional[str] = None,
                 fecha_adquisicion: Optional[date] = None, ubicacion_fisica: Optional[str] = None):
        self.id = id
        self.libro_id = libro_id
        self.codigo_ejemplar = codigo_ejemplar
        self.estado = estado  
        self.observaciones = observaciones
        self.fecha_adquisicion = fecha_adquisicion or date.today()
        self.ubicacion_fisica = ubicacion_fisica
        
        # Relación con libro
        self._libro = None
    
    @property
    def libro(self) -> Optional['Libro']:
        return self._libro
    
    @libro.setter
    def libro(self, valor: 'Libro'):
        self._libro = valor
    
    def puede_prestarse(self) -> bool:
        """Verifica si el ejemplar puede ser prestado."""
        return self.estado == 'disponible'
    
    def prestar(self) -> bool:
        """Marca el ejemplar como prestado."""
        if self.puede_prestarse():
            self.estado = 'prestado'
            return True
        return False
    
    def devolver(self) -> bool:
        """Marca el ejemplar como disponible."""
        if self.estado == 'prestado':
            self.estado = 'disponible'
            return True
        return False

class Prestamo:
    def __init__(self, id: int, ejemplar_id: int, usuario_id: int,
                 fecha_prestamo: Optional[date] = None, fecha_devolucion_esperada: Optional[date] = None,
                 fecha_devolucion_real: Optional[date] = None, estado: str = 'activo',
                 observaciones: Optional[str] = None, renovaciones: int = 0):
        self.id = id
        self.ejemplar_id = ejemplar_id
        self.usuario_id = usuario_id
        self.fecha_prestamo = fecha_prestamo or date.today()
        self.fecha_devolucion_esperada = fecha_devolucion_esperada
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado 
        self.observaciones = observaciones
        self.renovaciones = renovaciones
        
        # Relaciones
        self._ejemplar = None
        self._usuario = None
    
    @property
    def ejemplar(self) -> Optional['Ejemplar']:
        return self._ejemplar
    
    @ejemplar.setter
    def ejemplar(self, valor: 'Ejemplar'):
        self._ejemplar = valor
    
    @property
    def usuario(self) -> Optional['Usuario']:
        return self._usuario
    
    @usuario.setter
    def usuario(self, valor: 'Usuario'):
        self._usuario = valor
    
    @property
    def dias_prestamo(self) -> int:
        """Días transcurridos desde el préstamo."""
        return (date.today() - self.fecha_prestamo).days
    
    @property
    def esta_vencido(self) -> bool:
        """Verifica si el préstamo está vencido."""
        if self.fecha_devolucion_esperada and self.estado == 'activo':
            return date.today() > self.fecha_devolucion_esperada
        return False
    
    @property
    def dias_vencimiento(self) -> int:
        """Días de vencimiento (positivo si está vencido)."""
        if self.fecha_devolucion_esperada:
            return (date.today() - self.fecha_devolucion_esperada).days
        return 0
    
    def renovar(self, nuevos_dias: int = 15) -> bool:
        """Renueva el préstamo por días adicionales."""
        if self.estado == 'activo' and not self.esta_vencido:
            self.fecha_devolucion_esperada = date.today() + datetime.timedelta(days=nuevos_dias)
            self.renovaciones += 1
            return True
        return False
    
    def devolver(self) -> bool:
        """Marca el préstamo como devuelto."""
        if self.estado == 'activo':
            self.estado = 'devuelto'
            self.fecha_devolucion_real = date.today()
            return True
        return False