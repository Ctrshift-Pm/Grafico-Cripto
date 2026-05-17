import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.coingecko import get_global_data, STABLECOIN_IDS, TOP_ALT_IDS
from utils.calculations import calculate_adjusted_dominance
from charts.pie_chart import generate_pie_chart


class TestCryptoDominanceAPI(unittest.TestCase):
    """Testes unitários para o módulo de integração com a API da CoinGecko."""

    @patch('requests.get')
    def test_get_global_data_success(self, mock_get):
        """Verifica se get_global_data processa corretamente uma resposta bem sucedida da API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "total_market_cap": {"usd": 2500000000000.0},
                "market_cap_percentage": {
                    "btc": 54.20,
                    "eth": 17.10,
                    "usdt": 5.10,
                    "usdc": 1.90,
                    "bnb": 3.20,
                    "sol": 2.10,
                    "xrp": 1.20,
                    "doge": 0.90,
                    "others": 14.30
                }
            }
        }
        mock_get.return_value = mock_response

        result = get_global_data()

        self.assertEqual(result["total_market_cap"], 2500000000000.0)
        self.assertIn("btc", result["market_cap_percentage"])
        self.assertEqual(result["market_cap_percentage"]["btc"], 54.20)
        self.assertEqual(result["market_cap_percentage"]["eth"], 17.10)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_global_data_failure(self, mock_get):
        """Verifica se get_global_data lança uma exceção adequada ao receber erro de conexão/API."""
        mock_get.side_effect = Exception("Erro de conexão com o servidor")
        
        with self.assertRaises(Exception):
            get_global_data()


class TestCryptoDominanceCalculations(unittest.TestCase):
    """Testes unitários para o motor de cálculos matemáticos e dedução dos 5 segmentos."""

    def test_calculate_adjusted_dominance_mathematically_correct(self):
        """Verifica se o cálculo classifica e deduz corretamente os 5 pilares do mercado."""
        global_data = {
            "market_cap_percentage": {
                "btc": 54.00,
                "eth": 17.00,
                "usdt": 5.00,
                "usdc": 2.00,
                "bnb": 3.00,
                "sol": 2.50,
                "xrp": 1.50,
                "ada": 1.00,
                "doge": 1.00,
                "trx": 1.00,
            }
        }

        result = calculate_adjusted_dominance(global_data)

        self.assertEqual(result["Bitcoin"], 54.00)
        self.assertEqual(result["Ethereum"], 17.00)
        self.assertEqual(result["Stablecoins"], 7.00)
        self.assertEqual(result["Top 10 Alts"], 10.00)
        self.assertEqual(result["OTHERS"], 12.00)
        soma = sum(result.values())
        self.assertAlmostEqual(soma, 100.0, places=4)

    def test_calculate_adjusted_dominance_edge_case_empty(self):
        """Verifica estabilidade matemática e comportamento seguro com mapa de dominância vazio."""
        global_data = {"market_cap_percentage": {}}
        result = calculate_adjusted_dominance(global_data)
        
        self.assertEqual(result["Bitcoin"], 0.0)
        self.assertEqual(result["Ethereum"], 0.0)
        self.assertEqual(result["Stablecoins"], 0.0)
        self.assertEqual(result["Top 10 Alts"], 0.0)
        self.assertEqual(result["OTHERS"], 100.0)


class TestCryptoDominanceIntegration(unittest.TestCase):
    """Testes de integração simulando o fluxo de ponta a ponta do aplicativo."""

    @patch('requests.get')
    def test_end_to_end_flow(self, mock_get):
        """Verifica a integridade do pipeline completo: API Mock → Cálculo de Dominância → Rótulos do Gráfico."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "total_market_cap": {"usd": 3000000000000.0},
                "market_cap_percentage": {
                    "btc": 50.00,
                    "eth": 15.00,
                    "usdt": 6.00,
                    "usdc": 4.00,
                    "bnb": 5.00,
                    "sol": 3.00,
                    "xrp": 2.00,
                }
            }
        }
        mock_get.return_value = mock_response

        api_data = get_global_data()
        dominance = calculate_adjusted_dominance(api_data)

        self.assertEqual(dominance["Bitcoin"], 50.00)
        self.assertEqual(dominance["Ethereum"], 15.00)
        self.assertEqual(dominance["Stablecoins"], 10.00)
        self.assertEqual(dominance["Top 10 Alts"], 10.00)
        self.assertEqual(dominance["OTHERS"], 15.00)

        fig, ax = generate_pie_chart(dominance, save_path=None)
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)

        import matplotlib.pyplot as plt
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
