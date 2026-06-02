from abc import ABC, abstractmethod
from collections import deque
from dados import logs_telemetria
from typing import Dict, Tuple, Any, List
import json

class RegraValidacao(ABC):
    @abstractmethod
    def validar(self, valor: float, regras: Dict[str, float]) -> str:
        pass

class ValidacaoLimiteSimples(RegraValidacao):
    def validar(self, valor: float, regras: Dict[str, float]) -> str:
        if (valor < regras["critico_min"]) or (valor > regras["critico_max"]):
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

class MotorAnalise:
    def __init__(self, config: Dict[str, Dict[str, float]]) -> None:
        self.historico: Dict[str, deque[float]] = {sensor: deque(maxlen=3) for sensor in config.keys()}
        self.config: Dict[str, Dict[str, float]] = config
        self.regras: Dict[str, RegraValidacao] = {
            "limite_simples": ValidacaoLimiteSimples(),
            "limite_duplo": ValidacaoLimiteDuplo()
        }

    def adicionar_leitura(self, sensor: str, valor: float) -> Tuple[float, str]:
        buffer: deque[float] = self.historico[sensor]
        buffer.append(valor)
        media: float = sum(buffer) / len(buffer)

        info_limite: Dict[str, float] = self.config[sensor]

        if "alerta_min_inf" in info_limite:
            tipo: str = "limite_duplo"
        else:
            tipo = "limite_simples"

        status: str = self.regras[tipo].validar(media, info_limite)
        return media, status

def main() -> None:
    with open('config.json', 'r') as arquivo:
        config_sensores: Dict[str, Dict[str, float]] = json.load(arquivo)

    CORES_STATUS: Dict[str, str] = {
        "Normal": "\033[92mNormal\033[0m",
        "Alerta": "\033[93mAlerta\033[0m",
        "Crítico": "\033[91m\033[1mCRÍTICO\033[0m"
    }

    motor: MotorAnalise = MotorAnalise(config_sensores)
    logs: List[Dict[str, Any]] = logs_telemetria

    for log in logs:
        nome_sensor: str = log["sensor"]
        valor_numerico: float = float(log["leitura"])

        media, status = motor.adicionar_leitura(nome_sensor, valor_numerico)
        status_cor: str = CORES_STATUS.get(status, status)

        print(f"Sensor: {nome_sensor:<20} | Média Móvel: {media:<6.2f} | Status: {status_cor}")

if __name__ == "__main__":
    main()