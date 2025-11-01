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
        if not self.name.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"{self.name}: nombre debe ser alfanumérico (se permiten _ y -).")
        if not self.states:
            raise ValueError(f"{self.name}: conjunto de estados vacío.")
        if len(self.states) > 1000:  # Límite razonable
            raise ValueError(f"{self.name}: demasiados estados (máximo 1000).")
        if self.start is None or self.start not in self.states:
            raise ValueError(f"{self.name}: estado inicial inválido o ausente.")
        if not self.finals.issubset(self.states):
            raise ValueError(f"{self.name}: estados finales deben pertenecer a los estados.")
        if not self.alphabet:
            raise ValueError(f"{self.name}: alfabeto vacío.")
        if len(self.alphabet) > 100:  # Límite razonable
            raise ValueError(f"{self.name}: alfabeto demasiado grande (máximo 100 símbolos).")
        
        # Validar nombres de estados y símbolos
        for state in self.states:
            if not state or not isinstance(state, str) or len(state) > 50:
                raise ValueError(f"{self.name}: estado inválido: {state}")
        for symbol in self.alphabet:
            if not symbol or not isinstance(symbol, str) or len(symbol) > 10:
                raise ValueError(f"{self.name}: símbolo inválido: {symbol}")
        
        # Determinismo: no puede haber dos transiciones para (estado, símbolo)
        seen = set()
        for key in self.delta.keys():
            if key in seen:
                s, a = key
                raise ValueError(f"{self.name}: transición duplicada para ({s},{a}).")
            seen.add(key)
        
        # Validar todas las transiciones usan estados/símbolos válidos
        for (s, a), t in self.delta.items():
            if s not in self.states or t not in self.states:
                raise ValueError(f"{self.name}: transición con estado desconocido: {s}->{t}")
            if a not in self.alphabet:
                raise ValueError(f"{self.name}: transición usa símbolo fuera del alfabeto: {a}")
        
        # Verificar completitud opcional (función de transición total)
        self._check_completeness_warning()

        # Verificar completitud opcional (función de transición total)
        self._check_completeness_warning()

    def _check_completeness_warning(self) -> None:
        """Verifica si el AFD es completo (función de transición total)"""
        missing = []
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.delta:
                    missing.append(f"({state},{symbol})")
        if missing:
            import warnings
            warnings.warn(
                f"{self.name}: AFD incompleto. Transiciones faltantes: {', '.join(missing[:5])}"
                + ("..." if len(missing) > 5 else ""),
                UserWarning
            )

    def is_complete(self) -> bool:
        """Verifica si el AFD tiene función de transición total"""
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.delta:
                    return False
        return True

    def simulate(self, word: str, max_length: int = 10000) -> tuple[bool, List[str]]:
        """Devuelve (acepta, trayectoria_de_estados)."""
        self.validate()
        
        # Validación de entrada
        if not isinstance(word, str):
            return (False, ["#ERR:input_not_string"])
        if len(word) > max_length:
            return (False, [f"#ERR:word_too_long_{len(word)}>_{max_length}"])
        
        current = self.start
        path = [current]
        
        for i, ch in enumerate(word):
            if ch not in self.alphabet:
                # símbolo no reconocido => rechazo inmediato
                return (False, path + [f"#ERR:unknown_symbol_{ch}_at_pos_{i}"])
            
            nxt = self.delta.get((current, ch))
            if nxt is None:
                # Transición no definida - AFD incompleto
                return (False, path + [f"#TRAP:no_transition_from_{current}_with_{ch}"])
            
            current = nxt
            path.append(current)
            
            # Protección contra loops infinitos (aunque no debería pasar en AFD)
            if len(path) > max_length + 1:
                return (False, path + ["#ERR:simulation_too_long"])
        
        return (current in self.finals, path)

    def merge(self, other: "DFA") -> None:
        """Regla del enunciado: si el nombre ya existe, AGREGAR información."""
        if self.name != other.name:
            raise ValueError("Solo se pueden fusionar AFDs con el mismo nombre")
        
        # Validar que el otro DFA sea válido antes del merge
        other.validate()
        
        # Verificar compatibilidad de estados iniciales
        if self.start is not None and other.start is not None and self.start != other.start:
            raise ValueError(
                f"{self.name}: conflicto en estado inicial: {self.start} vs {other.start}"
            )
        
        # Unión de estados/alfabeto/finales
        old_states_count = len(self.states)
        old_alphabet_count = len(self.alphabet)
        
        self.states |= other.states
        self.alphabet |= other.alphabet
        self.finals |= other.finals
        
        # Si other tiene start definido y nosotros no, lo tomamos
        if other.start and not self.start:
            self.start = other.start
        elif other.start and self.start:
            # Ya verificamos que sean iguales arriba
            pass
        
        # Unir transiciones, respetando determinismo
        conflicts = []
        for k, v in other.delta.items():
            if k in self.delta and self.delta[k] != v:
                s, a = k
                conflicts.append(f"({s},{a}): {self.delta[k]} vs {v}")
            else:
                self.delta[k] = v
        
        if conflicts:
            raise ValueError(
                f"{self.name}: conflictos deterministas en transiciones: {', '.join(conflicts)}"
            )
        
        # Verificar límites después del merge
        if len(self.states) > 1000:
            raise ValueError(f"{self.name}: demasiados estados después del merge: {len(self.states)}")
        if len(self.alphabet) > 100:
            raise ValueError(f"{self.name}: alfabeto demasiado grande después del merge: {len(self.alphabet)}")
        
        # Log informativo sobre el merge
        import warnings
        new_states = len(self.states) - old_states_count
        new_symbols = len(self.alphabet) - old_alphabet_count
        if new_states > 0 or new_symbols > 0:
            warnings.warn(
                f"{self.name}: merge completado - agregados {new_states} estados, "
                f"{new_symbols} símbolos, {len(other.delta)} transiciones",
                UserWarning
            )
