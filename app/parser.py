from __future__ import annotations
from typing import Dict, List
from .dfa import DFA

# Formato: <IdInfo>:<Nombre>:<Info1>;<Info2>;...;<InfoN>
# IdInfo:
#   1 -> estados: q0,q1,q2
#   2 -> alfabeto: a,b
#   3 -> inicial: q0
#   4 -> finales: q1,q2
#   5 -> transiciones: q0,a,q1;q0,b,q2;...

def parse_line(line: str) -> tuple[int, str, List[str]]:
    line = line.strip()
    if not line or line.startswith("#"):
        raise ValueError("Línea vacía/comentario")
    try:
        head, rest = line.split(":", 1)
        name, info = rest.split(":", 1)
    except ValueError:
        raise ValueError(f"Formato inválido: {line}")
    try:
        idinfo = int(head)
    except ValueError:
        raise ValueError(f"IdInfo inválido: {head}")
    items = [x for x in info.split(";") if x != ""]
    return idinfo, name.strip(), items

def parse_file(filepath: str) -> Dict[str, DFA]:
    dfas: Dict[str, DFA] = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                idinfo, name, items = parse_line(raw)
            except ValueError:
                # permitir separadores en blanco u otras líneas sin romper el parseo
                continue

            dfa = dfas.get(name) or DFA(name=name)

            if idinfo == 1:
                # estados
                for st in ",".join(items).split(","):
                    if st:
                        dfa.states.add(st.strip())
            elif idinfo == 2:
                # alfabeto
                for s in ",".join(items).split(","):
                    if s:
                        dfa.alphabet.add(s.strip())
            elif idinfo == 3:
                # inicial (solo 1 esperado)
                dfa.start = items[0].strip() if items else dfa.start
            elif idinfo == 4:
                # finales
                for st in ",".join(items).split(","):
                    if st:
                        dfa.finals.add(st.strip())
            elif idinfo == 5:
                # transiciones: cada item: qI,a,qF
                for triple in items:
                    parts = [p.strip() for p in triple.split(",")]
                    if len(parts) != 3:
                        raise ValueError(f"Transición inválida: {triple}")
                    s, a, t = parts
                    if (s, a) in dfa.delta and dfa.delta[(s, a)] != t:
                        raise ValueError(
                            f"Conflicto determinista en {name} para ({s},{a})"
                        )
                    dfa.delta[(s, a)] = t
            else:
                raise ValueError(f"IdInfo desconocido: {idinfo}")

            dfas[name] = dfa

    # validar todos
    for d in dfas.values():
        d.validate()
    return dfas
