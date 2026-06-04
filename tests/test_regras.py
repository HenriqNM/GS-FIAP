import unittest
from typing import Dict
from src.regras import ValidacaoLimiteSimples, ValidacaoLimiteDuplo

class TestRegrasValidacao(unittest.TestCase):
    def setUp(self) -> None:
        self.regra_simples: ValidacaoLimiteSimples = ValidacaoLimiteSimples()
        self.regra_dupla: ValidacaoLimiteDuplo = ValidacaoLimiteDuplo()
        self.params_simples: Dict[str, float] = {
            "critico_min": 10.0,
            "critico_max": 50.0,
            "alerta_min": 20.0,
            "alerta_max": 30.0
        }
        self.params_duplos: Dict[str, float] = {
            "critico_min": 11.0,
            "critico_max": 15.0,
            "alerta_min_inf": 11.0,
            "alerta_max_inf": 11.9,
            "alerta_min_sup": 14.6,
            "alerta_max_sup": 15.0
        }

    def test_limite_simples_normal(self) -> None:
        status: str = self.regra_simples.validar(15.0, self.params_simples)
        self.assertEqual(status, 'Normal')

    def test_limite_simples_alerta(self) -> None:
        status: str = self.regra_simples.validar(25.0, self.params_simples)
        self.assertEqual(status, 'Alerta')

    def test_limite_simples_critico(self) -> None:
        status: str = self.regra_simples.validar(5.0, self.params_simples)
        self.assertEqual(status, 'Crítico')

    def test_limite_simples_fronteiras(self) -> None:
        self.assertEqual(self.regra_simples.validar(20.0, self.params_simples), 'Alerta')
        self.assertEqual(self.regra_simples.validar(30.0, self.params_simples), 'Alerta')

        self.assertEqual(self.regra_simples.validar(9.9999, self.params_simples), 'Crítico')
        self.assertEqual(self.regra_simples.validar(50.0001, self.params_simples), 'Crítico')

    def test_limite_duplo_normal(self) -> None:
        status: str = self.regra_dupla.validar(13.0, self.params_duplos)
        self.assertEqual(status, 'Normal')

    def test_limite_duplo_alerta_inferior(self) -> None:
        self.assertEqual(self.regra_dupla.validar(11.0, self.params_duplos), 'Alerta')
        self.assertEqual(self.regra_dupla.validar(11.5, self.params_duplos), 'Alerta')
        self.assertEqual(self.regra_dupla.validar(11.9, self.params_duplos), 'Alerta')

    def test_limite_duplo_alerta_superior(self) -> None:
        self.assertEqual(self.regra_dupla.validar(14.6, self.params_duplos), 'Alerta')
        self.assertEqual(self.regra_dupla.validar(14.8, self.params_duplos), 'Alerta')
        self.assertEqual(self.regra_dupla.validar(15.0, self.params_duplos), 'Alerta')

    def test_limite_duplo_critico_extremos(self) -> None:
        self.assertEqual(self.regra_dupla.validar(10.9, self.params_duplos), 'Crítico')
        self.assertEqual(self.regra_dupla.validar(15.1, self.params_duplos), 'Crítico')

    def test_limite_duplo_fronteira(self) -> None:
        self.assertEqual(self.regra_dupla.validar(10.99, self.params_duplos), 'Crítico')
        self.assertEqual(self.regra_dupla.validar(11.91, self.params_duplos), 'Normal')
        self.assertEqual(self.regra_dupla.validar(14.59, self.params_duplos), 'Normal')
        self.assertEqual(self.regra_dupla.validar(15.01, self.params_duplos), 'Crítico')

if __name__ == '__main__':
    unittest.main()