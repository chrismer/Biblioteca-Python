#!/usr/bin/env python3
"""
Script de debug para verificar el problema con insertar_estanteria
"""

from logic.library_manager import GestorBiblioteca

def test_insertar_estanteria():
    print("🔍 Depurando insertar_estanteria...")
    
    gestor = GestorBiblioteca()
    
    try:
        print("1. Creando estantería directamente en DB...")
        
        # Probar el método directamente en db_manager
        def _insert_debug(cursor):
            print(f"2. Ejecutando INSERT...")
            cursor.execute("INSERT INTO estanterias (nombre, capacidad) VALUES (?, ?)", ("Debug Test", 25))
            print(f"3. LastrowID: {cursor.lastrowid}")
            return cursor.lastrowid
        
        result = gestor.db.execute_transaction(_insert_debug)
        print(f"4. Resultado de execute_transaction: {result}")
        
        # Ahora probar el método normal
        print("\n5. Probando método normal...")
        result2 = gestor.agregar_estanteria("Debug Test 2", 30)
        print(f"6. Resultado de agregar_estanteria: {result2}")
        
        # Verificar en la base de datos
        print("\n7. Verificando en base de datos...")
        estanterias = gestor.get_todas_las_estanterias()
        print(f"8. Total de estanterías: {len(estanterias)}")
        for est in estanterias:
            if "Debug" in est.nombre:
                print(f"   - {est.id}: {est.nombre}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        gestor.cerrar()

if __name__ == "__main__":
    test_insertar_estanteria()
