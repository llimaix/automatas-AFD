#!/usr/bin/env python3
"""
Script para probar los 5 archivos de ejemplo con el sistema AFD mejorado.
Demuestra diferentes escenarios y casos de uso.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.store import AutomataStore
import warnings

def test_file(filename, test_cases):
    """Prueba un archivo específico con casos de prueba"""
    print(f"\n{'='*60}")
    print(f"🧪 PROBANDO: {filename}")
    print(f"{'='*60}")
    
    store = AutomataStore()
    
    try:
        # Cargar el archivo
        loaded = store.load_from_file(f"examples/{filename}")
        print(f"✅ Cargados {len(loaded)} autómatas: {', '.join(loaded)}")
        
        # Mostrar información de cada autómata
        for name in loaded:
            dfa = store.get(name)
            print(f"\n📋 {name}:")
            print(f"   Estados: {len(dfa.states)} - {sorted(list(dfa.states))}")
            print(f"   Alfabeto: {len(dfa.alphabet)} - {sorted(list(dfa.alphabet))}")
            print(f"   Inicial: {dfa.start}")
            print(f"   Finales: {sorted(list(dfa.finals))}")
            print(f"   Transiciones: {len(dfa.delta)}")
            print(f"   Completo: {'✅' if dfa.is_complete() else '⚠️  No'}")
        
        # Ejecutar casos de prueba
        print(f"\n🔍 CASOS DE PRUEBA:")
        for automata, word, expected in test_cases:
            if automata in loaded:
                try:
                    result = store.check(automata, word)
                    status = "✅" if result["accepted"] == expected else "❌"
                    print(f"   {status} {automata}('{word}') = {result['accepted']} (esperado: {expected})")
                    if not result["accepted"] and result["path"][-1].startswith("#"):
                        print(f"      Razón: {result['path'][-1]}")
                except Exception as e:
                    print(f"   ❌ Error en {automata}('{word}'): {e}")
    
    except Exception as e:
        print(f"❌ Error cargando {filename}: {e}")

def main():
    """Función principal de prueba"""
    print("🚀 PRUEBA DE ARCHIVOS DE EJEMPLO AFD")
    print("Sistema mejorado con validaciones robustas")
    
    # Configurar warnings
    warnings.simplefilter("always")
    
    # Ejemplo 1: AFDs Básicos
    test_file("ejemplo1_basico.txt", [
        ("TERMINA_EN_A", "abba", True),
        ("TERMINA_EN_A", "abbb", False),
        ("TERMINA_EN_A", "", False),
        ("DIV_POR_3", "11", True),  # 3 en binario
        ("DIV_POR_3", "110", True), # 6 en binario
        ("DIV_POR_3", "111", False), # 7 en binario
        ("SOLO_ABC", "abc", True),
        ("SOLO_ABC", "ab", False),
        ("SOLO_ABC", "abcd", False),
    ])
    
    # Ejemplo 2: AFDs Incompletos
    test_file("ejemplo2_incompletos.txt", [
        ("INCOMPLETO_1", "aa", True),
        ("INCOMPLETO_1", "ab", False),  # Transición faltante
        ("INCOMPLETO_2", "x", False),
        ("INCOMPLETO_2", "xy", False),
        ("INCOMPLETO_2", "xyz", False), # Transición faltante
        ("PARA_MERGE", "0", True),
        ("PARA_MERGE", "1", False),  # Inicialmente incompleto
    ])
    
    # Ejemplo 3: Testing de Merge
    test_file("ejemplo3_merge.txt", [
        ("PARA_MERGE", "0", True),
        ("PARA_MERGE", "1", False),
        ("PARA_MERGE", "012", True),
        ("PAR_A_Y_B", "", True),     # 0 a's, 0 b's (par)
        ("PAR_A_Y_B", "ab", True),   # 1 a, 1 b (ambos pares)
        ("PAR_A_Y_B", "a", False),   # 1 a (impar)
        ("ALFABETO_GRANDE", "a0a", True),
        ("ALFABETO_GRANDE", "b1e", True),
    ])
    
    # Ejemplo 4: Mundo Real
    test_file("ejemplo4_mundo_real.txt", [
        ("NUMERO_ENTERO", "123", True),
        ("NUMERO_ENTERO", "", False),
        ("NUMERO_ENTERO", "12a", False),  # Contiene letra
        ("IDENTIFICADOR", "var1", True),
        ("IDENTIFICADOR", "123", False),  # Empieza con número
        ("IDENTIFICADOR", "", False),
        ("COMENTARIO", "slash", False),
        ("COMENTARIO", "slashslash", True),
        ("COMENTARIO", "slashslasha", True),
    ])
    
    # Ejemplo 5: Casos Extremos
    test_file("ejemplo5_casos_extremos.txt", [
        ("SOLO_VACIO", "", True),
        ("SOLO_VACIO", "a", False),
        ("NUNCA_ACEPTA", "", False),
        ("NUNCA_ACEPTA", "ab", False),
        ("MUCHOS_FINALES", "x", True),
        ("MUCHOS_FINALES", "xy", True),
        ("INICIAL_ES_FINAL", "", True),
        ("INICIAL_ES_FINAL", "go", False),
        ("ESTADOS_LARGOS", "simbolo_a", False),
        ("ESTADOS_LARGOS", "simbolo_asimbol_b", True),
    ])
    
    print(f"\n🎉 PRUEBAS COMPLETADAS")
    print("\n📝 Ejemplos incluidos:")
    print("1. ejemplo1_basico.txt - AFDs fundamentales completos")
    print("2. ejemplo2_incompletos.txt - AFDs con transiciones faltantes") 
    print("3. ejemplo3_merge.txt - Testing de merge y alfabetos grandes")
    print("4. ejemplo4_mundo_real.txt - Validadores de patrones prácticos")
    print("5. ejemplo5_casos_extremos.txt - Límites y casos edge")

if __name__ == "__main__":
    main()