from typing import List, Dict, Any, Tuple
from src.motor import MotorAnalise

def processar_telemetria(logs: list, motor: MotorAnalise) -> dict[str, tuple[list[int], list[float]]]:
    historico_sensores: Dict[str, Tuple[List[int], List[float]]] = {}
    contadores_sensores: Dict[str, int] = {}

    CORES_STATUS: Dict[str, str] = {
        "Normal": "\033[92mNormal\033[0m",
        "Alerta": "\033[93mAlerta\033[0m",
        "Crítico": "\033[91m\033[1mCRÍTICO\033[0m",
        "Dado corrompido": "\033[90mDado corrompido\033[0m"
    }

    print("=" * 60)
    print(f"      \033[96mPROCESSAMENTO DOS LOGS DE TELEMETRIA\033[0m       ")
    print("=" * 60)

    for log in logs:
        try:
            nome_sensor: str = log["sensor"]
            valor_numerico: float = float(log["leitura"])
            media, status = motor.adicionar_leitura(nome_sensor, valor_numerico)

            if nome_sensor not in historico_sensores:
                historico_sensores[nome_sensor] = ([], [])
                contadores_sensores[nome_sensor] = 0

            contadores_sensores[nome_sensor] += 1
            historico_sensores[nome_sensor][0].append(contadores_sensores[nome_sensor])
            historico_sensores[nome_sensor][1].append(media)

        except (ValueError, KeyError, TypeError):
            nome_sensor = log["sensor"] if isinstance(log, dict) and "sensor" in log else "Desconhecido"
            media = 0.0
            status = "Dado corrompido"

        status_cor: str = CORES_STATUS.get(status, status)
        print(f"Sensor: {nome_sensor:<20} | Média Móvel: {media:<6.2f} | Status: {status_cor}")

    return historico_sensores