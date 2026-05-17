import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://api.coingecko.com/api/v3"

HEADERS = {
    "accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

STABLECOIN_IDS = {
    "usdt", "usdc", "dai", "busd", "fdusd", "tusd", "usde",
    "usdp", "gusd", "lusd", "frax", "usdd", "susd", "cusd",
}

TOP_ALT_IDS = {
    "bnb", "sol", "xrp", "ada", "doge", "trx", "avax", "ton",
    "link", "shib", "dot", "ltc", "bch", "uni", "near", "icp",
    "matic", "xlm", "atom", "apt", "hbar", "vet", "fil",
}


def get_global_data():
    """
    Busca dados globais do mercado cripto na CoinGecko.
    Retorna market cap total e o mapa completo de dominância por moeda.
    """
    url = f"{BASE_URL}/global"
    logger.info("Buscando dados globais do mercado em CoinGecko...")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json().get("data", {})

        total_market_cap     = data.get("total_market_cap", {}).get("usd", 0)
        market_cap_percentage = data.get("market_cap_percentage", {})

        if total_market_cap == 0:
            raise ValueError("Market Cap retornado foi zero.")

        logger.info(
            f"Dados globais OK. Total: ${total_market_cap:,.0f}  |  "
            f"BTC: {market_cap_percentage.get('btc', 0):.2f}%  "
            f"ETH: {market_cap_percentage.get('eth', 0):.2f}%"
        )
        return {
            "total_market_cap":      total_market_cap,
            "market_cap_percentage": market_cap_percentage,
        }

    except Exception as e:
        logger.error(f"Erro ao buscar dados globais: {e}")
        raise


def get_stablecoin_market_cap():
    """
    Mantido para compatibilidade retroativa — não é mais usado no cálculo
    principal (os dados vêm do market_cap_percentage do /global).
    Retorna 0 para não afetar o fluxo.
    """
    return 0.0
