from collections import deque
from typing import Dict, Tuple, Any
import regras

class MotorAnalise:
    def __init__(self, config: Dict[str, Dict[str, Any]]) -> None:
        self.historico: Dict[str, deque[float]] = {sensor: deque(maxlen=3) for sensor in config.keys()}
        self.config: Dict[str, Dict[str, float]] = config

    def adicionar_leitura(self, sensor: str, valor: float) -> Tuple[float, str]:
        try:
            if sensor not in self.historico:
                return 0.0, "Dado corrompido"

            buffer: deque[float] = self.historico[sensor]
            valor_float: float = float(valor)
            buffer.append(valor_float)
            media: float = sum(buffer) / len(buffer)

            if sensor not in self.config:
                return media, "Dado corrompido"

            info_limite: Dict[str, float] = self.config[sensor]
            nome_classe: str = info_limite["regra_classe"]
            valores: Dict[str, float] = info_limite["parametros"]
            try:
                instancia_regra = getattr(regras, nome_classe)()
            except AttributeError:
                return media, "Dado corrompido"

            try:
                status: str = instancia_regra.validar(media, valores)
                return media, status
            except Exception:
                return media, "Dado corrompido"

        except (ValueError, KeyError, TypeError):
            return 0.0, "Dado corrompido"