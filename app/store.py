from __future__ import annotations
from typing import Dict, List
from .dfa import DFA
from .parser import parse_file

class AutomataStore:
    def __init__(self) -> None:
        self._dfas: Dict[str, DFA] = {}

    def load_from_file(self, path: str) -> List[str]:
        parsed = parse_file(path)
        loaded: List[str] = []
        for name, newdfa in parsed.items():
            if name in self._dfas:
                self._dfas[name].merge(newdfa)
            else:
                self._dfas[name] = newdfa
            loaded.append(name)
        # validar tras merges
        for dfa in self._dfas.values():
            dfa.validate()
        return loaded

    def list(self) -> List[str]:
        return sorted(self._dfas.keys())

    def get(self, name: str) -> DFA:
        if name not in self._dfas:
            raise KeyError(f"No existe el autómata: {name}")
        return self._dfas[name]

    def check(self, name: str, word: str) -> dict:
        dfa = self.get(name)
        ok, path = dfa.simulate(word)
        return {
            "automata": name,
            "word": word,
            "accepted": ok,
            "path": path
        }

# Singleton sencillo para API/CLI
store = AutomataStore()
