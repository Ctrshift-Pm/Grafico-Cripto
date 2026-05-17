import logging
from api.coingecko import STABLECOIN_IDS, TOP_ALT_IDS

logger = logging.getLogger(__name__)


def calculate_adjusted_dominance(global_data, _stable_cap_unused=0):
    """
    Calcula a dominância precisa de 5 segmentos do mercado cripto usando
    o mapa completo de market_cap_percentage retornado pelo endpoint /global.

    Segmentos:
        Bitcoin     — BTC individual
        Ethereum    — ETH individual
        Stablecoins — USDT, USDC, DAI e demais stablecoins conhecidas
        Top 10 Alts — BNB, SOL, XRP, ADA, DOGE, TRX, AVAX, TON, etc.
        OTHERS      — Resíduo: 100% - (soma dos 4 acima)

    Retorna dicionário com as 5 chaves e seus respectivos % brutos
    (não renormalizados — somam 100% do mercado total).
    """
    mcp = global_data.get("market_cap_percentage", {})

    btc_pct = mcp.get("btc", 0.0)
    eth_pct = mcp.get("eth", 0.0)

    stable_pct = sum(
        v for k, v in mcp.items()
        if k in STABLECOIN_IDS
    )

    top_alt_pct = sum(
        v for k, v in mcp.items()
        if k in TOP_ALT_IDS
    )

    others_pct = max(0.0, 100.0 - btc_pct - eth_pct - stable_pct - top_alt_pct)

    logger.info("─── Dominância Precisa (5 Segmentos) ─────────────────")
    logger.info(f"  Bitcoin:     {btc_pct:.4f}%")
    logger.info(f"  Ethereum:    {eth_pct:.4f}%")
    logger.info(f"  Stablecoins: {stable_pct:.4f}%")
    logger.info(f"  Top 10 Alts: {top_alt_pct:.4f}%")
    logger.info(f"  OTHERS.D:    {others_pct:.4f}%")
    logger.info(f"  SOMA TOTAL:  {btc_pct+eth_pct+stable_pct+top_alt_pct+others_pct:.4f}%")
    logger.info("──────────────────────────────────────────────────────")

    return {
        "Bitcoin":     btc_pct,
        "Ethereum":    eth_pct,
        "Stablecoins": stable_pct,
        "Top 10 Alts": top_alt_pct,
        "OTHERS":      others_pct,
    }
