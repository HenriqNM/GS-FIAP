from abc import ABC, abstractmethod
from collections import deque
from dados import logs_telemetria
import json

class RegraValidacao(ABC):
    @abstractmethod
    def validar(self, valor, regras):
        pass

class ValidacaoLimiteSimples(RegraValidacao):
    def validar(self, valor, regras):
        if (valor < regras["critico_min"]) or (valor > regras["critico_max"]):
            return 'Crítico'
        if regras["alerta_min"] <= valor <= regras["alerta_max"]:
            return 'Alerta'
        return 'Normal'

class ValidacaoLimiteDuplo(RegraValidacao):
    def validar(self, valor, regras):
        if valor < regras["critico_min"] or valor > regras["critico_max"]:
            return 'Crítico'
        if (regras["alerta_min_inf"] <= valor <= regras["alerta_max_inf"]) or (regras["alerta_min_sup"] <= valor <= regras["alerta_max_sup"]):
            return 'Alerta'
        return 'Normal'

class MotorAnalise:
    def __init__(self, config):
        self.historico = {sensor: deque(maxlen=3) for sensor in config.keys()}
        self.config = config
        self.regras = {
            "limite_simples": ValidacaoLimiteSimples(),
            "limite_duplo": ValidacaoLimiteDuplo()
        }

    def adicionar_leitura(self, sensor, valor):
        buffer = self.historico[sensor]
        buffer.append(valor)
        media = sum(buffer) / len(buffer)

        info_limite = self.config[sensor]

        if "alerta_min_inf" in info_limite:
            tipo = "limite_duplo"
        else:
            tipo = "limite_simples"
        status = self.regras[tipo].validar(media, info_limite)
        return media, status

def main():
    with open('config.json', 'r') as arquivo:
        config_sensores = json.load(arquivo)

    CORES_STATUS = {
        "Normal": "\033[92mNormal\033[0m",  # Verde
        "Alerta": "\033[93mAlerta\033[0m",  # Amarelo
        "Crítico": "\033[91m\033[1mCRÍTICO\033[0m"  # Vermelho Negrito
    }

    motor = MotorAnalise(config_sensores)

    for log in logs_telemetria:
        nome_sensor = log["sensor"]
        valor_numerico = float(log["leitura"])

        media, status = motor.adicionar_leitura(nome_sensor, valor_numerico)
        status_cor = CORES_STATUS.get(status, status)

        print(f"Sensor: {nome_sensor:<20} | Média Móvel: {media:<6.2f} | Status: {status_cor}")

if __name__ == "__main__":
    main()