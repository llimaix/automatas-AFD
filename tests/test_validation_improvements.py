"""
Tests para las mejoras de validación y robustez del sistema AFD
"""
import pytest
import tempfile
import os
from app.dfa import DFA
from app.parser import parse_file, parse_line
from app.store import AutomataStore

def test_dfa_limits_validation():
    """Test de límites en validación de DFA"""
    
    # Test: demasiados estados
    dfa = DFA(name="test")
    dfa.states = {f"q{i}" for i in range(1001)}  # Más del límite
    dfa.alphabet = {"a"}
    dfa.start = "q0"
    dfa.finals = {"q0"}
    
    with pytest.raises(ValueError, match="demasiados estados"):
        dfa.validate()

def test_dfa_name_validation():
    """Test de validación de nombres"""
    
    # Nombre inválido con caracteres especiales
    dfa = DFA(name="test@#$")
    dfa.states = {"q0"}
    dfa.alphabet = {"a"}
    dfa.start = "q0"
    dfa.finals = {"q0"}
    
    with pytest.raises(ValueError, match="nombre debe ser alfanumérico"):
        dfa.validate()

def test_dfa_completeness_check():
    """Test de verificación de completitud"""
    
    # DFA incompleto
    dfa = DFA(name="incomplete")
    dfa.states = {"q0", "q1"}
    dfa.alphabet = {"a", "b"}
    dfa.start = "q0"
    dfa.finals = {"q1"}
    dfa.delta = {("q0", "a"): "q1"}  # Falta transición (q0,b) y (q1,a), (q1,b)
    
    assert not dfa.is_complete()
    
    # Completar el DFA
    dfa.delta[("q0", "b")] = "q0"
    dfa.delta[("q1", "a")] = "q1"
    dfa.delta[("q1", "b")] = "q0"
    
    assert dfa.is_complete()

def test_word_length_limits():
    """Test de límites en longitud de palabras"""
    
    dfa = DFA(name="test")
    dfa.states = {"q0", "q1"}
    dfa.alphabet = {"a"}
    dfa.start = "q0"
    dfa.finals = {"q1"}
    dfa.delta = {("q0", "a"): "q1", ("q1", "a"): "q0"}
    
    # Palabra muy larga
    long_word = "a" * 10001
    accepted, path = dfa.simulate(long_word, max_length=100)
    
    assert not accepted
    assert "word_too_long" in path[0]

def test_parser_security():
    """Test de seguridad del parser"""
    
    # Línea demasiado larga
    long_line = "1:test:" + "q" * 10001
    with pytest.raises(ValueError, match="demasiado larga"):
        parse_line(long_line)
    
    # Nombre inválido
    invalid_name_line = "1:test@#$:q0,q1"
    with pytest.raises(ValueError, match="Nombre inválido"):
        parse_line(invalid_name_line)
    
    # Demasiados elementos
    many_items = "1:test:" + ";".join([f"q{i}" for i in range(1001)])
    with pytest.raises(ValueError, match="Demasiados elementos"):
        parse_line(many_items)

def test_merge_conflicts():
    """Test de conflictos en merge de AFDs"""
    
    # Crear dos AFDs con conflicto en estado inicial
    dfa1 = DFA(name="test")
    dfa1.states = {"q0", "q1"}
    dfa1.alphabet = {"a"}
    dfa1.start = "q0"
    dfa1.finals = {"q1"}
    dfa1.delta = {("q0", "a"): "q1"}
    
    dfa2 = DFA(name="test")
    dfa2.states = {"q0", "q1"}
    dfa2.alphabet = {"a"}
    dfa2.start = "q1"  # Diferente estado inicial
    dfa2.finals = {"q1"}
    dfa2.delta = {("q1", "a"): "q0"}
    
    with pytest.raises(ValueError, match="conflicto en estado inicial"):
        dfa1.merge(dfa2)

def test_large_file_protection():
    """Test de protección contra archivos grandes"""
    
    # Crear archivo temporal muy grande
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        # Escribir contenido que exceda el límite
        for i in range(15000):  # Más de 10000 líneas
            f.write(f"1:test{i}:q{i}\n")
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError, match="demasiadas líneas"):
            parse_file(temp_path)
    finally:
        os.unlink(temp_path)

def test_unknown_symbols_simulation():
    """Test de simulación con símbolos desconocidos"""
    
    dfa = DFA(name="test")
    dfa.states = {"q0", "q1"}
    dfa.alphabet = {"a"}
    dfa.start = "q0"
    dfa.finals = {"q1"}
    dfa.delta = {("q0", "a"): "q1"}
    
    # Probar con símbolo no en el alfabeto
    accepted, path = dfa.simulate("ab")
    
    assert not accepted
    assert "unknown_symbol_b_at_pos_1" in path[-1]

def test_store_error_handling():
    """Test de manejo de errores en el store"""
    
    store = AutomataStore()
    
    # Intentar obtener autómata inexistente
    with pytest.raises(KeyError, match="No existe el autómata"):
        store.get("nonexistent")
    
    # Probar check con autómata inexistente
    with pytest.raises(KeyError):
        store.check("nonexistent", "test")

if __name__ == "__main__":
    pytest.main([__file__])