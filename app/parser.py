from __future__ import annotations
from typing import Dict, List
import re
from .dfa import DFA

# Formato: <IdInfo>:<Nombre>:<Info1>;<Info2>;...;<InfoN>
# IdInfo:
#   1 -> estados: q0,q1,q2
#   2 -> alfabeto: a,b
#   3 -> inicial: q0
#   4 -> finales: q1,q2
#   5 -> transiciones: q0,a,q1;q0,b,q2;...

# Límites de seguridad
MAX_LINE_LENGTH = 10000
MAX_ITEMS_PER_LINE = 1000
MAX_FILE_SIZE = 1024 * 1024  # 1MB

def sanitize_name(name: str) -> str:
    """Sanitiza y valida nombres de autómatas"""
    if not name or len(name) > 100:
        raise ValueError(f"Nombre inválido: longitud debe ser 1-100 caracteres")
    # Solo permitir alfanuméricos, guiones y guiones bajos
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        raise ValueError(f"Nombre inválido: {name}. Solo se permiten letras, números, _ y -")
    return name.strip()

def sanitize_identifier(identifier: str, max_len: int = 50) -> str:
    """Sanitiza identificadores (estados, símbolos)"""
    if not identifier or len(identifier) > max_len:
        raise ValueError(f"Identificador inválido: longitud debe ser 1-{max_len}")
    # Permitir más caracteres para símbolos pero restringir caracteres peligrosos
    if not re.match(r'^[a-zA-Z0-9_-]+$', identifier):
        raise ValueError(f"Identificador inválido: {identifier}")
    return identifier.strip()

def parse_line(line: str) -> tuple[int, str, List[str]]:
    line = line.strip()
    if not line or line.startswith("#"):
        raise ValueError("Línea vacía/comentario")
    
    if len(line) > MAX_LINE_LENGTH:
        raise ValueError(f"Línea demasiado larga: {len(line)} > {MAX_LINE_LENGTH}")
    
    try:
        parts = line.split(":", 2)  # Limitar splits para evitar problemas
        if len(parts) != 3:
            raise ValueError(f"Formato inválido: se esperan exactamente 2 ':' en la línea")
        
        head, name, info = parts
    except ValueError:
        raise ValueError(f"Formato inválido: {line}")
    
    try:
        idinfo = int(head)
        if idinfo not in [1, 2, 3, 4, 5]:
            raise ValueError(f"IdInfo debe ser 1-5, recibido: {idinfo}")
    except ValueError:
        raise ValueError(f"IdInfo inválido: {head}")
    
    # Sanitizar nombre
    name = sanitize_name(name)
    
    # Procesar información con límites
    items = [x.strip() for x in info.split(";") if x.strip()]
    if len(items) > MAX_ITEMS_PER_LINE:
        raise ValueError(f"Demasiados elementos en línea: {len(items)} > {MAX_ITEMS_PER_LINE}")
    
    return idinfo, name, items

def parse_file(filepath: str) -> Dict[str, DFA]:
    import os
    
    # Verificar tamaño del archivo
    if os.path.getsize(filepath) > MAX_FILE_SIZE:
        raise ValueError(f"Archivo demasiado grande: {os.path.getsize(filepath)} bytes > {MAX_FILE_SIZE}")
    
    dfas: Dict[str, DFA] = {}
    line_count = 0
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, raw in enumerate(f, 1):
            line_count += 1
            if line_count > 10000:  # Límite de líneas
                raise ValueError("Archivo tiene demasiadas líneas (máximo 10000)")
            
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
                
            try:
                idinfo, name, items = parse_line(raw)
            except ValueError as e:
                raise ValueError(f"Error en línea {line_num}: {e}")

            # Obtener o crear DFA
            if name not in dfas:
                dfas[name] = DFA(name=name)
            dfa = dfas[name]

            try:
                if idinfo == 1:
                    # estados
                    states_str = ",".join(items)
                    for st in states_str.split(","):
                        st = st.strip()
                        if st:
                            dfa.states.add(sanitize_identifier(st))
                            
                elif idinfo == 2:
                    # alfabeto
                    alphabet_str = ",".join(items)
                    for s in alphabet_str.split(","):
                        s = s.strip()
                        if s:
                            # Los símbolos pueden ser más flexibles pero limitados
                            if len(s) > 10:
                                raise ValueError(f"Símbolo demasiado largo: {s}")
                            dfa.alphabet.add(s)
                            
                elif idinfo == 3:
                    # inicial (solo 1 esperado)
                    if len(items) != 1:
                        raise ValueError("Se esperaba exactamente un estado inicial")
                    initial = sanitize_identifier(items[0])
                    dfa.start = initial
                    
                elif idinfo == 4:
                    # finales
                    finals_str = ",".join(items)
                    for st in finals_str.split(","):
                        st = st.strip()
                        if st:
                            dfa.finals.add(sanitize_identifier(st))
                            
                elif idinfo == 5:
                    # transiciones: cada item: qI,a,qF
                    for triple in items:
                        parts = [p.strip() for p in triple.split(",")]
                        if len(parts) != 3:
                            raise ValueError(f"Transición inválida: {triple} (se esperan 3 elementos)")
                        
                        s, a, t = parts
                        s = sanitize_identifier(s)
                        t = sanitize_identifier(t)
                        
                        # El símbolo 'a' puede ser más flexible
                        if not a or len(a) > 10:
                            raise ValueError(f"Símbolo de transición inválido: {a}")
                        
                        if (s, a) in dfa.delta and dfa.delta[(s, a)] != t:
                            raise ValueError(
                                f"Conflicto determinista en {name} para ({s},{a}): "
                                f"ya existe {dfa.delta[(s, a)]}, se intenta agregar {t}"
                            )
                        dfa.delta[(s, a)] = t
                        
            except ValueError as e:
                raise ValueError(f"Error procesando {name} en línea {line_num}: {e}")

    # Validar todos los DFAs
    for name, dfa in dfas.items():
        try:
            dfa.validate()
        except ValueError as e:
            raise ValueError(f"Error validando DFA {name}: {e}")
    
    return dfas
