from __future__ import annotations
from typing import Dict, List
from .dfa import DFA
from .parser import parse_file
import os
import logging

logger = logging.getLogger(__name__)

class AutomataStore:
    def __init__(self) -> None:
        self._dfas: Dict[str, DFA] = {}
        self._default_file = "/app/data/automatas.txt"

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

    def _load_default_automatas(self):
        """Carga autómatas por defecto desde data/automatas.txt solo al inicio"""
        try:
            if os.path.exists(self._default_file):
                logger.info("Cargando autómatas por defecto desde data/automatas.txt")
                loaded = self.load_from_file(self._default_file)
                logger.info(f"Autómatas por defecto cargados: {loaded}")
                return len(loaded) > 0
        except Exception as e:
            logger.error(f"Error cargando autómatas por defecto: {e}")
        return False

    def initialize(self):
        """Inicializa el store cargando solo autómatas por defecto una vez"""
        try:
            # Solo cargar autómatas por defecto al inicio del servidor
            if self._load_default_automatas():
                logger.info("Store inicializado con autómatas por defecto")
                return
            
            logger.info("Store inicializado vacío - no hay autómatas disponibles")
            
        except Exception as e:
            logger.error(f"Error inicializando store: {e}")

    def clear_all(self):
        """Limpia todos los autómatas de la memoria"""
        try:
            self._dfas.clear()
            logger.info("Todos los autómatas limpiados de memoria")
        except Exception as e:
            logger.error(f"Error limpiando autómatas: {e}")

    def reset_to_defaults(self):
        """Resetea a los autómatas por defecto"""
        try:
            self.clear_all()
            self._load_default_automatas()
            logger.info("Store reseteado a autómatas por defecto")
        except Exception as e:
            logger.error(f"Error reseteando a defaults: {e}")

    def list(self) -> List[str]:
        return sorted(self._dfas.keys())

    def get(self, name: str) -> DFA:
        if name not in self._dfas:
            raise KeyError(f"No existe el autómata: {name}")
        return self._dfas[name]

    def check(self, name: str, word: str, max_length: int = 10000) -> dict:
        dfa = self.get(name)
        ok, path = dfa.simulate(word, max_length=max_length)
        return {
            "automata": name,
            "word": word,
            "accepted": ok,
            "path": path
        }

# Singleton sencillo para API/CLI
store = AutomataStore()
