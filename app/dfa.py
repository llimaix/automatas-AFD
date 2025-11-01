from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Set, Tuple, List

Transition = Dict[Tuple[str, str], str]

@dataclass
class DFA:
    name: str
    states: Set[str] = field(default_factory=set)
    alphabet: Set[str] = field(default_factory=set)
    start: str | None = None
    finals: Set[str] = field(default_factory=set)
    delta: Transition = field(default_factory=dict)

    def validate(self) -> None:
        if not self.name:
            raise ValueError("El AFD debe tener nombre.")
        if not self.states:
            raise ValueError(f"{self.name}: conjunto de estados vacío.")
        if self.start is None or self.start not in self.states:
            raise ValueError(f"{self.name}: estado inicial inválido o ausente.")
        if not self.finals.issubset(self.states):
            raise ValueError(f"{self.name}: estados finales deben pertenecer a los estados.")
        # Determinismo: no puede haber dos transiciones para (estado, símbolo)
        seen = set()
        for key in self.delta.keys():
            if key in seen:
                s, a = key
                raise ValueError(f"{self.name}: transición duplicada para ({s},{a}).")
            seen.add(key)
        # Opcional: asegurar que todas las transiciones usan estados/símbolos válidos
        for (s, a), t in self.delta.items():
            if s not in self.states or t not in self.states:
                raise ValueError(f"{self.name}: transición con estado desconocido: {s}->{t}")
            if a not in self.alphabet:
                raise ValueError(f"{self.name}: transición usa símbolo fuera del alfabeto: {a}")

    def simulate(self, word: str) -> tuple[bool, List[str]]:
        """Devuelve (acepta, trayectoria_de_estados)."""
        self.validate()
        current = self.start
        path = [current]
        for ch in word:
            if ch not in self.alphabet:
                # símbolo no reconocido => rechazo inmediato
                return (False, path + [f"#ERR:{ch}"])
            nxt = self.delta.get((current, ch))
            if nxt is None:
                return (False, path + [f"#TRAP:{current},{ch}"])
            current = nxt
            path.append(current)
        return (current in self.finals, path)

    def merge(self, other: "DFA") -> None:
        """Regla del enunciado: si el nombre ya existe, AGREGAR información."""
        if self.name != other.name:
            raise ValueError("Solo se pueden fusionar AFDs con el mismo nombre")
        # Unión de estados/alfabeto/finales
        self.states |= other.states
        self.alphabet |= other.alphabet
        self.finals |= other.finals
        # Si other tiene start definido, lo tomamos como override razonable
        if other.start:
            self.start = other.start
        # Unir transiciones, respetando determinismo (no sobrescribir inconsistente)
        for k, v in other.delta.items():
            if k in self.delta and self.delta[k] != v:
                s, a = k
                raise ValueError(
                    f"{self.name}: conflicto determinista en ({s},{a}): "
                    f"{self.delta[k]} vs {v}"
                )
            self.delta[k] = v
