from abc import ABC, abstractmethod
from typing import Dict

class RegraValidacao(ABC):
    @abstractmethod
    def validar(self, valor: float, regras: Dict[str, float]) -> str:
        pass

class ValidacaoLimiteSimples(RegraValidacao):
    def validar(self, valor: float, regras: Dict[str, float]) -> str:
        if valor < regras["critico_min"] or valor > regras["critico_max"]:
            return 'Crítico'
        if regras["alerta_min"] <= valor <= regras["alerta_max"]:
            return 'Alerta'
        return 'Normal'

class ValidacaoLimiteDuplo(RegraValidacao):
    def validar(self, valor: float, regras: Dict[str, float]) -> str:
        if valor < regras["critico_min"] or valor > regras["critico_max"]:
            return 'Crítico'
        if (regras["alerta_min_inf"] <= valor <= regras["alerta_max_inf"]) or (
                regras["alerta_min_sup"] <= valor <= regras["alerta_max_sup"]):
            return 'Alerta'
        return 'Normal'