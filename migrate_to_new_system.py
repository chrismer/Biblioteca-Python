#!/usr/bin/env python3
"""
Script de migración del sistema anterior al nuevo
Crea ejemplares individuales para todos los libros existentes
"""

import sqlite3
from datetime import date

def migrar_sistema():
    """Migra del sistema anterior al nuevo creando ejemplares individuales."""
    print("🔄 Iniciando migración del sistema legacy al nuevo...")
    
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # 1. Verificar qué libros ya tienen ejemplares
        cursor.execute("""
            SELECT l.id, l.codigo, l.titulo, l.cantidad_total, l.cantidad_prestados,
                   COUNT(e.id) as ejemplares_existentes
            FROM libros l
            LEFT JOIN ejemplares e ON l.id = e.libro_id
            GROUP BY l.id
        """)
        libros = cursor.fetchall()
        
        print(f"📚 Encontrados {len(libros)} libros para procesar...")
        
        libros_migrados = 0
        ejemplares_creados = 0
        
        for libro in libros:
            libro_id = libro['id']
            codigo = libro['codigo']
            titulo = libro['titulo']
            cantidad_total = libro['cantidad_total'] or 0
            cantidad_prestados = libro['cantidad_prestados'] or 0
            ejemplares_existentes = libro['ejemplares_existentes']
            
            print(f"\n📖 Procesando: {codigo} - {titulo}")
            print(f"   Total: {cantidad_total}, Prestados: {cantidad_prestados}, Ejemplares existentes: {ejemplares_existentes}")
            
            # Solo crear ejemplares si no existen
            if ejemplares_existentes == 0 and cantidad_total > 0:
                # Crear ejemplares individuales
                for i in range(cantidad_total):
                    codigo_ejemplar = f"{codigo}-{i+1:03d}"  # Ej: LIB001-001, LIB001-002
                    
                    # Determinar estado del ejemplar
                    if i < cantidad_prestados:
                        estado = 'prestado'
                    else:
                        estado = 'disponible'
                    
                    cursor.execute("""
                        INSERT INTO ejemplares (libro_id, codigo_ejemplar, estado, fecha_adquisicion)
                        VALUES (?, ?, ?, ?)
                    """, (libro_id, codigo_ejemplar, estado, date.today()))
                    
                    ejemplares_creados += 1
                    print(f"   ✅ Creado ejemplar: {codigo_ejemplar} ({estado})")
                
                libros_migrados += 1
            elif ejemplares_existentes > 0:
                print(f"   ⚠️ Ya tiene {ejemplares_existentes} ejemplares, omitiendo...")
            else:
                print(f"   ⚠️ No tiene cantidad_total definida, omitiendo...")
        
        # 2. Verificar resultados
        cursor.execute("SELECT COUNT(*) FROM ejemplares")
        total_ejemplares = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ejemplares WHERE estado = 'disponible'")
        disponibles = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ejemplares WHERE estado = 'prestado'")
        prestados = cursor.fetchone()[0]
        
        conn.commit()
        
        print(f"\n🎉 MIGRACIÓN COMPLETADA:")
        print(f"   📚 Libros migrados: {libros_migrados}")
        print(f"   📦 Ejemplares creados: {ejemplares_creados}")
        print(f"   📊 Total ejemplares en sistema: {total_ejemplares}")
        print(f"   ✅ Disponibles: {disponibles}")
        print(f"   📤 Prestados: {prestados}")
        
        if ejemplares_creados > 0:
            print(f"\n💡 Ahora el botón 'Detalles' mostrará ejemplares individuales")
            print(f"   y podrás usar el sistema de préstamos profesional!")
        else:
            print(f"\n💡 Todos los libros ya tenían ejemplares individuales.")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def verificar_sistema():
    """Verifica el estado actual del sistema."""
    print("🔍 Verificando estado del sistema...")
    
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Verificar tablas
        cursor.execute("SELECT COUNT(*) FROM libros")
        total_libros = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ejemplares")
        total_ejemplares = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM prestamos")
        total_prestamos = cursor.fetchone()[0]
        
        print(f"📊 ESTADO ACTUAL:")
        print(f"   📚 Libros: {total_libros}")
        print(f"   📦 Ejemplares: {total_ejemplares}")
        print(f"   👥 Usuarios: {total_usuarios}")
        print(f"   🔄 Préstamos: {total_prestamos}")
        
        # Mostrar algunos ejemplos
        cursor.execute("""
            SELECT l.codigo, l.titulo, COUNT(e.id) as ejemplares
            FROM libros l
            LEFT JOIN ejemplares e ON l.id = e.libro_id
            GROUP BY l.id
            LIMIT 5
        """)
        
        print(f"\n📋 EJEMPLOS DE LIBROS:")
        for row in cursor.fetchall():
            print(f"   {row['codigo']}: {row['titulo']} ({row['ejemplares']} ejemplares)")
            
    except Exception as e:
        print(f"❌ Error verificando sistema: {e}")
    finally:
        conn.close()

def main():
    """Función principal."""
    print("=" * 60)
    print("     🔄 MIGRACIÓN AL SISTEMA NUEVO")
    print("=" * 60)
    
    verificar_sistema()
    
    print(f"\n" + "=" * 60)
    respuesta = input("\n¿Desea migrar al sistema nuevo? (s/N): ")
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        migrar_sistema()
        print(f"\n" + "=" * 60)
        print("✅ Migración completada. Reinicie la aplicación para ver los cambios.")
    else:
        print("❌ Migración cancelada.")

if __name__ == "__main__":
    main()
