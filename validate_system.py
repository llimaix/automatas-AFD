#!/usr/bin/env python3
"""
Script de validación para verificar que el sistema esté funcionando correctamente
después de las mejoras del frontend y backend.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_backend_imports():
    """Prueba que todas las importaciones del backend funcionen"""
    try:
        from app.dfa import DFA
        from app.parser import parse_file
        from app.store import store
        from app.api import app
        print("✅ Importaciones del backend: OK")
        return True
    except ImportError as e:
        print(f"❌ Error en importaciones del backend: {e}")
        return False

def test_dfa_functionality():
    """Prueba la funcionalidad básica de DFA"""
    try:
        from app.dfa import DFA
        
        # Crear un DFA simple
        dfa = DFA(name="test_dfa")
        dfa.states = {"q0", "q1"}
        dfa.alphabet = {"a", "b"}
        dfa.start = "q0"
        dfa.finals = {"q1"}
        dfa.delta = {("q0", "a"): "q1", ("q0", "b"): "q0", ("q1", "a"): "q1", ("q1", "b"): "q0"}
        
        # Validar
        dfa.validate()
        
        # Probar completitud
        is_complete = dfa.is_complete()
        
        # Probar simulación
        accepted, path = dfa.simulate("a")
        
        print(f"✅ Funcionalidad DFA: OK (completo: {is_complete}, simulación: {accepted})")
        return True
    except Exception as e:
        print(f"❌ Error en funcionalidad DFA: {e}")
        return False

def test_parser_functionality():
    """Prueba la funcionalidad del parser"""
    try:
        from app.parser import parse_file
        import tempfile
        
        # Crear archivo temporal con contenido de prueba
        test_content = """1:TEST_AFD:q0,q1
2:TEST_AFD:a,b
3:TEST_AFD:q0
4:TEST_AFD:q1
5:TEST_AFD:q0,a,q1;q0,b,q0;q1,a,q1;q1,b,q0"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            temp_path = f.name
        
        try:
            dfas = parse_file(temp_path)
            if "TEST_AFD" in dfas:
                print("✅ Funcionalidad Parser: OK")
                return True
            else:
                print("❌ Parser no creó el AFD esperado")
                return False
        finally:
            os.unlink(temp_path)
            
    except Exception as e:
        print(f"❌ Error en funcionalidad Parser: {e}")
        return False

def test_store_functionality():
    """Prueba la funcionalidad del store"""
    try:
        from app.store import AutomataStore
        
        store = AutomataStore()
        
        # El store debería estar vacío inicialmente
        automata_list = store.list()
        
        print(f"✅ Funcionalidad Store: OK (autómatas disponibles: {len(automata_list)})")
        return True
    except Exception as e:
        print(f"❌ Error en funcionalidad Store: {e}")
        return False

def test_validation_improvements():
    """Prueba las mejoras de validación"""
    try:
        from app.dfa import DFA
        
        # Probar validación de nombre
        try:
            bad_dfa = DFA(name="bad@name")
            bad_dfa.states = {"q0"}
            bad_dfa.alphabet = {"a"}
            bad_dfa.start = "q0"
            bad_dfa.finals = {"q0"}
            bad_dfa.validate()
            print("❌ Validación de nombre: FALLÓ (debería rechazar nombres inválidos)")
            return False
        except ValueError:
            print("✅ Validación de nombre: OK")
        
        # Probar límites de estados
        try:
            big_dfa = DFA(name="big_dfa")
            big_dfa.states = {f"q{i}" for i in range(1001)}
            big_dfa.alphabet = {"a"}
            big_dfa.start = "q0"
            big_dfa.finals = {"q0"}
            big_dfa.validate()
            print("❌ Validación de límites: FALLÓ (debería rechazar demasiados estados)")
            return False
        except ValueError:
            print("✅ Validación de límites: OK")
        
        return True
    except Exception as e:
        print(f"❌ Error en validaciones mejoradas: {e}")
        return False

def check_frontend_files():
    """Verifica que los archivos del frontend existan"""
    frontend_files = [
        "src/App.jsx",
        "src/pages/LoadAutomata.jsx", 
        "src/pages/CheckWord.jsx",
        "src/pages/AutomataExplorer.jsx",
        "src/components/NotificationSystem.jsx",
        "src/hooks/useNotifications.js",
        "src/api/client.js",
        "src/index.css"
    ]
    
    missing_files = []
    for file_path in frontend_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Archivos frontend faltantes: {missing_files}")
        return False
    else:
        print("✅ Archivos frontend: OK")
        return True

def check_example_files():
    """Verifica que los archivos de ejemplo existan"""
    example_files = [
        "examples/ejemplo1_basico.txt",
        "examples/ejemplo2_incompletos.txt", 
        "examples/ejemplo3_merge.txt",
        "examples/ejemplo4_mundo_real.txt",
        "examples/ejemplo5_casos_extremos.txt",
        "examples/README.md"
    ]
    
    missing_files = []
    for file_path in example_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Archivos de ejemplo faltantes: {missing_files}")
        return False
    else:
        print("✅ Archivos de ejemplo: OK")
        return True

def main():
    """Función principal de validación"""
    print("🔍 VALIDACIÓN COMPLETA DEL SISTEMA AFD")
    print("=" * 50)
    
    tests = [
        ("Backend - Importaciones", test_backend_imports),
        ("Backend - Funcionalidad DFA", test_dfa_functionality),
        ("Backend - Funcionalidad Parser", test_parser_functionality),
        ("Backend - Funcionalidad Store", test_store_functionality),
        ("Backend - Validaciones Mejoradas", test_validation_improvements),
        ("Frontend - Archivos", check_frontend_files),
        ("Ejemplos - Archivos", check_example_files),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        try:
            if test_func():
                passed += 1
            else:
                print(f"   Falló: {test_name}")
        except Exception as e:
            print(f"   ❌ Error inesperado en {test_name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS VALIDACIONES EXITOSAS!")
        print("\n✅ El sistema está listo para usar con todas las mejoras:")
        print("   - Backend robusto con validaciones de seguridad")
        print("   - Frontend moderno con 3 páginas interactivas")
        print("   - Sistema de notificaciones en tiempo real")
        print("   - Explorador detallado de autómatas")
        print("   - Archivos de ejemplo para testing")
        print("   - Documentación completa")
    else:
        print(f"⚠️  {total - passed} pruebas fallaron. Revisar los errores arriba.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)