from pathlib import Path
from typing import Dict, Any, List
from .dados import logs_telemetria
from .motor import MotorAnalise
import json

def main() -> None:
    diretorio: Path = Path(__file__).parent.resolve()
    config: Path = diretorio.parent / "config.json"

    with open(config, 'r') as arquivo:
        config_sensores: Dict[str, Dict[str, Any]] = json.load(arquivo)

    CORES_STATUS: Dict[str, str] = {
        "Normal": "\033[92mNormal\033[0m",
        "Alerta": "\033[93mAlerta\033[0m",
        "Crítico": "\033[91m\033[1mCRÍTICO\033[0m",
        "Dado corrompido": "\033[90mDado corrompido\033[0m"
    }

    motor: MotorAnalise = MotorAnalise(config_sensores)
    logs: List[Any] = logs_telemetria

    for log in logs:
        try:
            nome_sensor: str = log["sensor"]
            valor_numerico: float = float(log["leitura"])

            media, status = motor.adicionar_leitura(nome_sensor, valor_numerico)

        except (ValueError, KeyError, TypeError):
            nome_sensor = log["sensor"] if isinstance(log, dict) and "sensor" in log else "Desconhecido"
            media = 0.0
            status = "Dado corrompido"

        status_cor: str = CORES_STATUS.get(status, status)
        print(f"Sensor: {nome_sensor:<20} | Média Móvel: {media:<6.2f} | Status: {status_cor}")

if __name__ == "__main__":
    main()