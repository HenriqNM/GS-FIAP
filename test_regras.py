import unittest
from typing import Dict
from regras import ValidacaoLimiteSimples, ValidacaoLimiteDuplo

class TestRegrasValidacao(unittest.TestCase):
    def setUp(self) -> None:
        self.regra_simples: ValidacaoLimiteSimples = ValidacaoLimiteSimples()
        self.regra_dupla: ValidacaoLimiteDuplo = ValidacaoLimiteDuplo()

    def test_limite_simples_normal(self) -> None:
        parametros: Dict[str, float] = {
            "critico_min": 10.0,
            "critico_max": 50.0,
            "alerta_min": 20.0,
            "alerta_max": 30.0
        }
        status: str = self.regra_simples.validar(15.0, parametros)
        self.assertEqual(status, 'Normal')

    def test_limite_simples_alerta(self) -> None:
        parametros: Dict[str, float] = {
            "critico_min": 10.0,
            "critico_max": 50.0,
            "alerta_min": 20.0,
            "alerta_max": 30.0
        }
        status: str = self.regra_simples.validar(25.0, parametros)
        self.assertEqual(status, 'Alerta')

    def test_limite_simples_critico(self) -> None:
        parametros: Dict[str, float] = {
            "critico_min": 10.0,
            "critico_max": 50.0,
            "alerta_min": 20.0,
            "alerta_max": 30.0
        }
        status: str = self.regra_simples.validar(5.0, parametros)
        self.assertEqual(status, 'Crítico')

if __name__ == '__main__':
    unittest.main()