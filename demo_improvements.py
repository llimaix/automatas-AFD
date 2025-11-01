#!/usr/bin/env python3
"""
Script de demostración de las mejoras de validación en el sistema AFD.
Ejecuta varios casos de prueba para mostrar la robustez mejorada.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.store import store
from app.dfa import DFA
import warnings

def demo_completeness_validation():
    """Demuestra la validación de completitud de AFDs"""
    print("=== DEMO: Validación de Completitud ===")
    
    # Cargar AFDs de prueba
    try:
        loaded = store.load_from_file("data/test_validation.txt")
        print(f"✓ Cargados: {loaded}")
        
        # Verificar completitud
        for name in loaded:
            dfa = store.get(name)
            is_complete = dfa.is_complete()
            print(f"  {name}: {'Completo' if is_complete else 'Incompleto'}")
            
    except Exception as e:
        print(f"✗ Error: {e}")

def demo_enhanced_simulation():
    """Demuestra la simulación mejorada con mejor manejo de errores"""
    print("\n=== DEMO: Simulación Mejorada ===")
    
    try:
        # Probar con símbolo no válido
        result = store.check("COMPLETE_AFD", "abc")  # 'c' no está en el alfabeto
        print(f"✓ Símbolo inválido detectado: {result['path'][-1]}")
        
        # Probar con palabra muy larga (limitada)
        long_word = "a" * 50
        result = store.check("COMPLETE_AFD", long_word, max_length=20)
        print(f"✓ Palabra procesada (limitada): acepta={result['accepted']}, path_length={len(result['path'])}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

def demo_security_features():
    """Demuestra las características de seguridad mejoradas"""
    print("\n=== DEMO: Características de Seguridad ===")
    
    # Intentar crear DFA con nombre inválido
    try:
        bad_dfa = DFA(name="bad@name")
        bad_dfa.states = {"q0"}
        bad_dfa.alphabet = {"a"}
        bad_dfa.start = "q0"
        bad_dfa.finals = {"q0"}
        bad_dfa.validate()
        print("✗ No se detectó nombre inválido")
    except ValueError as e:
        print(f"✓ Nombre inválido detectado: {e}")
    
    # Intentar crear DFA con demasiados estados
    try:
        big_dfa = DFA(name="big_dfa")
        big_dfa.states = {f"q{i}" for i in range(1001)}
        big_dfa.alphabet = {"a"}
        big_dfa.start = "q0"
        big_dfa.finals = {"q0"}
        big_dfa.validate()
        print("✗ No se detectó exceso de estados")
    except ValueError as e:
        print(f"✓ Exceso de estados detectado: {e}")

def demo_merge_improvements():
    """Demuestra las mejoras en el merge de AFDs"""
    print("\n=== DEMO: Mejoras en Merge ===")
    
    try:
        # El merge ya fue hecho al cargar el archivo
        merge_dfa = store.get("MERGE_TEST")
        print(f"✓ Merge exitoso:")
        print(f"  Estados: {sorted(merge_dfa.states)}")
        print(f"  Alfabeto: {sorted(merge_dfa.alphabet)}")
        print(f"  Transiciones: {len(merge_dfa.delta)}")
        print(f"  Completo: {merge_dfa.is_complete()}")
        
    except Exception as e:
        print(f"✗ Error en merge: {e}")

def main():
    """Función principal de demostración"""
    print("🔧 DEMOSTRACIÓN DE MEJORAS DE VALIDACIÓN AFD")
    print("=" * 50)
    
    # Configurar warnings para mostrar avisos de completitud
    warnings.simplefilter("always")
    
    demo_completeness_validation()
    demo_enhanced_simulation()
    demo_security_features()
    demo_merge_improvements()
    
    print("\n🎉 Demostración completada!")
    print("\nMejoras implementadas:")
    print("- ✅ Validación de límites de tamaño")
    print("- ✅ Sanitización de nombres e identificadores")
    print("- ✅ Detección de AFDs incompletos")
    print("- ✅ Simulación con límites configurables")
    print("- ✅ Manejo robusto de errores")
    print("- ✅ Logging detallado")
    print("- ✅ Merge mejorado con validaciones")
    print("- ✅ Protección contra archivos maliciosos")

if __name__ == "__main__":
    main()