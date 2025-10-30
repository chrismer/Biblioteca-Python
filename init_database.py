#!/usr/bin/env python3
"""
Script de inicialización de la base de datos con datos de prueba
Ejecutar este script una vez para poblar la base de datos con datos iniciales
"""

import sys
import os
from datetime import date
from logic.library_manager import GestorBiblioteca

def inicializar_datos_prueba():
    """Inicializa la base de datos con datos de prueba."""
    print("🚀 Inicializando base de datos con datos de prueba...")
    
    gestor = GestorBiblioteca()
    
    try:
        # 1. Crear estanterías
        print("\n📚 Creando estanterías...")
        estanterias = [
            ("Ficción", 20),
            ("No Ficción", 15),
            ("Ciencias", 25),
            ("Historia", 18),
            ("Literatura Clásica", 30)
        ]
        
        estanteria_ids = {}
        for nombre, capacidad in estanterias:
            try:
                estanteria_id = gestor.agregar_estanteria(nombre, capacidad)
                estanteria_ids[nombre] = estanteria_id
                print(f"  ✅ Estantería '{nombre}' creada (ID: {estanteria_id})")
            except Exception as e:
                print(f"  ⚠️ Estantería '{nombre}' ya existe o error: {e}")
                # Buscar la estantería existente
                estanterias_existentes = gestor.get_todas_estanterias()
                for est in estanterias_existentes:
                    if est.nombre == nombre:
                        estanteria_ids[nombre] = est.id
                        break
        
        # 2. Crear géneros
        print("\n🎭 Creando géneros...")
        generos = [
            ("Realismo Mágico", "Literatura que combina realidad con elementos fantásticos"),
            ("Ciencia Ficción", "Narrativa basada en avances científicos y tecnológicos"),
            ("Ensayo", "Texto de reflexión sobre diversos temas"),
            ("Biografía", "Relato de la vida de una persona"),
            ("Historia", "Narrativa de hechos pasados"),
            ("Filosofía", "Reflexión sobre la existencia y el conocimiento"),
            ("Romance", "Narrativa centrada en relaciones amorosas"),
            ("Thriller", "Narrativa de suspense y tensión")
        ]
        
        for nombre, descripcion in generos:
            try:
                genero_id = gestor.agregar_genero(nombre, descripcion)
                print(f"  ✅ Género '{nombre}' creado (ID: {genero_id})")
            except Exception as e:
                print(f"  ⚠️ Género '{nombre}' ya existe o error: {e}")
        
        # 3. Crear usuarios
        print("\n👥 Creando usuarios...")
        usuarios = [
            ("Ana García", "ana.garcia@email.com", "555-0101", "Calle Principal 123"),
            ("Carlos López", "carlos.lopez@email.com", "555-0102", "Av. Central 456"),
            ("María Rodríguez", "maria.rodriguez@email.com", "555-0103", "Plaza Mayor 789"),
            ("Juan Pérez", "juan.perez@email.com", "555-0104", "Barrio Norte 321"),
            ("Laura Martínez", "laura.martinez@email.com", "555-0105", "Zona Sur 654")
        ]
        
        for nombre, email, telefono, direccion in usuarios:
            try:
                usuario_id = gestor.agregar_usuario(nombre, email, telefono, direccion)
                print(f"  ✅ Usuario '{nombre}' creado (ID: {usuario_id})")
            except Exception as e:
                print(f"  ⚠️ Usuario '{nombre}' ya existe o error: {e}")
        
        # 4. Crear libros con ejemplares
        print("\n📖 Creando libros...")
        libros = [
            {
                "codigo": "LIB001",
                "titulo": "Cien Años de Soledad",
                "autor_nombre": "Gabriel",
                "autor_apellido": "García Márquez",
                "anio": 1967,
                "cantidad_ejemplares": 3,
                "estanteria": "Literatura Clásica",
                "genero": "Realismo Mágico",
                "isbn": "978-84-376-0494-7",
                "editorial": "Sudamericana"
            },
            {
                "codigo": "LIB002",
                "titulo": "1984",
                "autor_nombre": "George",
                "autor_apellido": "Orwell",
                "anio": 1949,
                "cantidad_ejemplares": 2,
                "estanteria": "Ficción",
                "genero": "Ciencia Ficción",
                "isbn": "978-84-376-0495-4",
                "editorial": "Planeta"
            },
            {
                "codigo": "LIB003",
                "titulo": "El Principito",
                "autor_nombre": "Antoine",
                "autor_apellido": "de Saint-Exupéry",
                "anio": 1943,
                "cantidad_ejemplares": 4,
                "estanteria": "Literatura Clásica",
                "genero": "Filosofía",
                "isbn": "978-84-376-0496-1",
                "editorial": "Salamandra"
            },
            {
                "codigo": "LIB004",
                "titulo": "Sapiens",
                "autor_nombre": "Yuval Noah",
                "autor_apellido": "Harari",
                "anio": 2011,
                "cantidad_ejemplares": 2,
                "estanteria": "No Ficción",
                "genero": "Historia",
                "isbn": "978-84-376-0497-8",
                "editorial": "Debate"
            },
            {
                "codigo": "LIB005",
                "titulo": "Don Quijote de la Mancha",
                "autor_nombre": "Miguel",
                "autor_apellido": "de Cervantes",
                "anio": 1605,
                "cantidad_ejemplares": 2,
                "estanteria": "Literatura Clásica",
                "genero": "Literatura Clásica",
                "isbn": "978-84-376-0498-5",
                "editorial": "Cátedra"
            }
        ]
        
        for libro_data in libros:
            try:
                libro_id = gestor.agregar_libro_simple(
                    codigo=libro_data["codigo"],
                    titulo=libro_data["titulo"],
                    autor_nombre=libro_data["autor_nombre"],
                    autor_apellido=libro_data["autor_apellido"],
                    anio=libro_data["anio"],
                    cantidad_ejemplares=libro_data["cantidad_ejemplares"],
                    estanteria_id=estanteria_ids[libro_data["estanteria"]],
                    genero_nombre=libro_data["genero"],
                    isbn=libro_data["isbn"],
                    editorial=libro_data["editorial"]
                )
                print(f"  ✅ Libro '{libro_data['titulo']}' creado con {libro_data['cantidad_ejemplares']} ejemplares (ID: {libro_id})")
            except Exception as e:
                print(f"  ⚠️ Libro '{libro_data['titulo']}' ya existe o error: {e}")
        
        # 5. Mostrar resumen final
        print("\n📊 RESUMEN DE LA INICIALIZACIÓN")
        resumen = gestor.get_resumen_biblioteca()
        print(f"  📚 Total de libros: {resumen['total_libros']}")
        print(f"  📖 Total de ejemplares: {resumen['total_ejemplares']}")
        print(f"  ✅ Ejemplares disponibles: {resumen['ejemplares_disponibles']}")
        print(f"  👥 Usuarios registrados: {resumen['usuarios_activos']}")
        print(f"  🏗️ Estanterías: {len(estanteria_ids)}")
        
        print("\n🎉 ¡Inicialización completada con éxito!")
        print("   Ahora puedes ejecutar la aplicación con: python main.py")
        
    except Exception as e:
        print(f"\n❌ Error durante la inicialización: {e}")
        raise
    finally:
        gestor.cerrar()

def main():
    """Función principal."""
    print("=" * 60)
    print("     🏛️ SISTEMA DE BIBLIOTECA - INICIALIZACIÓN")
    print("=" * 60)
    
    # Verificar si ya existe la base de datos
    if os.path.exists("biblioteca.db"):
        respuesta = input("\n⚠️ La base de datos ya existe. ¿Desea continuar? (s/N): ")
        if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Inicialización cancelada.")
            return
    
    try:
        inicializar_datos_prueba()
    except KeyboardInterrupt:
        print("\n❌ Inicialización interrumpida por el usuario.")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
