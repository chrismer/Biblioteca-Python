#!/usr/bin/env python3
"""
Script para actualizar ubicaciones de ejemplares existentes
Asigna ubicaciones automáticas basadas en la estantería del libro
"""

import sqlite3
from typing import Dict, List

def actualizar_ubicaciones():
    """Actualiza las ubicaciones de todos los ejemplares existentes."""
    print("🔄 Iniciando actualización de ubicaciones...")
    
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # 1. Obtener información de estanterías
        cursor.execute("SELECT id, nombre FROM estanterias ORDER BY id")
        estanterias = {row['id']: row['nombre'] for row in cursor.fetchall()}
        
        print(f"📚 Estanterías encontradas: {len(estanterias)}")
        for est_id, nombre in estanterias.items():
            print(f"   {est_id}: {nombre}")
        
        # 2. Obtener ejemplares sin ubicación específica
        cursor.execute("""
            SELECT e.id, e.codigo_ejemplar, e.libro_id, 
                   l.titulo, l.estanteria_id, est.nombre as estanteria_nombre
            FROM ejemplares e
            JOIN libros l ON e.libro_id = l.id
            JOIN estanterias est ON l.estanteria_id = est.id
            WHERE e.ubicacion_fisica IS NULL OR e.ubicacion_fisica = 'No especificada'
        """)
        
        ejemplares_sin_ubicacion = cursor.fetchall()
        print(f"\n📦 Ejemplares sin ubicación específica: {len(ejemplares_sin_ubicacion)}")
        
        if not ejemplares_sin_ubicacion:
            print("✅ Todos los ejemplares ya tienen ubicación asignada.")
            return
        
        # 3. Agrupar ejemplares por estantería para generar ubicaciones ordenadas
        ejemplares_por_estanteria = {}
        for ejemplar in ejemplares_sin_ubicacion:
            est_id = ejemplar['estanteria_id']
            if est_id not in ejemplares_por_estanteria:
                ejemplares_por_estanteria[est_id] = []
            ejemplares_por_estanteria[est_id].append(ejemplar)
        
        # 4. Generar ubicaciones sistemáticas
        ejemplares_actualizados = 0
        
        for est_id, ejemplares in ejemplares_por_estanteria.items():
            est_nombre = estanterias[est_id]
            print(f"\n📍 Procesando estantería: {est_nombre}")
            
            # Ordenar ejemplares por código para ubicación consistente
            ejemplares.sort(key=lambda x: x['codigo_ejemplar'])
            
            # Generar ubicaciones con formato: "Estantería [Nombre] - Nivel X - Pos Y"
            for i, ejemplar in enumerate(ejemplares, 1):
                # Calcular nivel y posición (asumiendo 10 libros por nivel)
                nivel = ((i - 1) // 10) + 1
                posicion = ((i - 1) % 10) + 1
                
                ubicacion = f"Estantería {est_nombre} - Nivel {nivel} - Pos {posicion}"
                
                # Actualizar en la base de datos
                cursor.execute("""
                    UPDATE ejemplares 
                    SET ubicacion_fisica = ? 
                    WHERE id = ?
                """, (ubicacion, ejemplar['id']))
                
                print(f"   ✅ {ejemplar['codigo_ejemplar']}: {ubicacion}")
                ejemplares_actualizados += 1
        
        # 5. Verificar resultados
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN ubicacion_fisica IS NOT NULL AND ubicacion_fisica != 'No especificada' THEN 1 ELSE 0 END) as con_ubicacion
            FROM ejemplares
        """)
        
        stats = cursor.fetchone()
        
        conn.commit()
        
        print(f"\n🎉 ACTUALIZACIÓN COMPLETADA:")
        print(f"   📦 Ejemplares actualizados: {ejemplares_actualizados}")
        print(f"   📊 Total ejemplares: {stats['total']}")
        print(f"   📍 Con ubicación: {stats['con_ubicacion']}")
        print(f"   ✅ Porcentaje completado: {(stats['con_ubicacion']/stats['total']*100):.1f}%")
        
        print(f"\n💡 Ahora la ventana 'Detalles' mostrará ubicaciones específicas")
        print(f"   como 'Estantería A - Nivel 1 - Pos 3'")
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def verificar_ubicaciones():
    """Verifica el estado actual de las ubicaciones."""
    print("🔍 Verificando estado de ubicaciones...")
    
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Estadísticas generales
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN ubicacion_fisica IS NOT NULL AND ubicacion_fisica != 'No especificada' THEN 1 ELSE 0 END) as con_ubicacion,
                SUM(CASE WHEN ubicacion_fisica IS NULL OR ubicacion_fisica = 'No especificada' THEN 1 ELSE 0 END) as sin_ubicacion
            FROM ejemplares
        """)
        
        stats = cursor.fetchone()
        
        print(f"📊 ESTADO ACTUAL:")
        print(f"   📦 Total ejemplares: {stats['total']}")
        print(f"   📍 Con ubicación: {stats['con_ubicacion']}")
        print(f"   ❓ Sin ubicación: {stats['sin_ubicacion']}")
        
        # Ejemplos de ubicaciones
        cursor.execute("""
            SELECT codigo_ejemplar, ubicacion_fisica 
            FROM ejemplares 
            WHERE ubicacion_fisica IS NOT NULL AND ubicacion_fisica != 'No especificada'
            LIMIT 5
        """)
        
        ejemplos = cursor.fetchall()
        if ejemplos:
            print(f"\n📋 EJEMPLOS DE UBICACIONES:")
            for ejemplo in ejemplos:
                print(f"   {ejemplo['codigo_ejemplar']}: {ejemplo['ubicacion_fisica']}")
                
    except Exception as e:
        print(f"❌ Error verificando ubicaciones: {e}")
    finally:
        conn.close()

def main():
    """Función principal."""
    print("=" * 70)
    print("     📍 ACTUALIZACIÓN DE UBICACIONES")
    print("=" * 70)
    
    verificar_ubicaciones()
    
    print(f"\n" + "=" * 70)
    respuesta = input("\n¿Desea actualizar las ubicaciones? (s/N): ")
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        actualizar_ubicaciones()
        print(f"\n" + "=" * 70)
        print("✅ Actualización completada. Reinicie la aplicación para ver los cambios.")
    else:
        print("❌ Actualización cancelada.")

if __name__ == "__main__":
    main()
