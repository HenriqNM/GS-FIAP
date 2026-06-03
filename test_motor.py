import unittest
from typing import Dict, Any, Tuple
from motor import MotorAnalise

class TestMotorAnaliseDefensivo(unittest.TestCase):
    def setUp(self) -> None:
        self.config_teste: Dict[str, Dict[str, Any]] = {
            "bateria_m1": {
                "regra_classe": "ValidacaoLimiteDuplo",
                "parametros": {
                    "critico_min": 11.0, "critico_max": 15.0,
                    "alerta_min_inf": 11.0, "alerta_max_inf": 11.9,
                    "alerta_min_sup": 14.6, "alerta_max_sup": 15.0
                }
            }
        }
        self.motor: MotorAnalise = MotorAnalise(self.config_teste)

    def test_sensor_inexistente_na_configuracao(self) -> None:
        resultado: Tuple[float, str] = self.motor.adicionar_leitura("sensor_desconhecido", 12.0)
        media, status = resultado

        self.assertEqual(status, "Dado corrompido")
        self.assertEqual(media, 0.0)

    def test_tipo_de_dado_invalido(self) -> None:
        media: float
        status: str
        media, status = self.motor.adicionar_leitura("bateria_m1", "TEXTO_INVALIDO")  # type: ignore

        self.assertEqual(status, "Dado corrompido")
        self.assertEqual(media, 0.0)