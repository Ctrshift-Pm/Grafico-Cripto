import os
import math
import logging
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from utils.image_loader import load_image_asset

logger = logging.getLogger(__name__)

BG_COLOR = "#000000"
COLOR_BTC = "#FCD535"
COLOR_ETH = "#4D70FF"
COLOR_STABLE = "#26A17B"
COLOR_ALT = "#FF7A00"
COLOR_OTHERS = "#BF5AF2"

LOCAL_LOGO_FILES = {
    "Bitcoin":     "bitcoin.png",
    "Ethereum":    "ethereum.png",
    "Stablecoins": "tether.png",
    "Top 10 Alts": "doge.png",
    "OTHERS":      "others.svg"
}

LOGO_CONFIG = {
    "Bitcoin":     {"max_size": 48, "radius": 0.68},
    "Ethereum":    {"max_size": 34, "radius": 0.68},
    "Stablecoins": {"max_size": 34, "radius": 0.68},
    "Top 10 Alts": {"max_size": 36, "radius": 0.68},
    "OTHERS":      {"max_size": 48, "radius": 0.68}
}


def _add_logo_fallback(ax, x, y, name, color):
    marker = "◉" if name != "OTHERS" else "◎"
    ax.text(
        x,
        y,
        marker,
        color=color,
        fontsize=20,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=12,
    )


def get_images_dir():
    """Retorna o caminho absoluto robusto do diretório de imagens local."""
    import sys
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "images")
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        images_dir = os.path.abspath(os.path.join(exe_dir, "..", "images"))
        if not os.path.exists(images_dir):
            images_dir = os.path.join(exe_dir, "images")
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.abspath(os.path.join(current_dir, "..", "images"))
        
    return images_dir


def generate_pie_chart(dominance_data, save_path=None):
    """
    Gera o gráfico de dominância preciso com 5 fatias no estilo donut premium Apple.
    Retorna os objetos fig e ax para integração em tempo real na GUI Tkinter.
    """
    logger.info("Iniciando geração do gráfico donut de 5 fatias...")
    images_dir = get_images_dir()

    categories = ["Bitcoin", "Ethereum", "Stablecoins", "Top 10 Alts", "OTHERS"]
    sizes = [dominance_data[cat] for cat in categories]
    colors = [COLOR_BTC, COLOR_ETH, COLOR_STABLE, COLOR_ALT, COLOR_OTHERS]

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['SF Pro Display', 'Inter', 'Helvetica Neue', 'Helvetica', 'Arial', 'DejaVu Sans']
    plt.style.use("dark_background")

    fig, ax = plt.subplots(figsize=(7.5, 7.5), facecolor=BG_COLOR)
    fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)
    ax.set_facecolor(BG_COLOR)

    wedgeprops = {
        "edgecolor": BG_COLOR,
        "linewidth": 8,
        "antialiased": True,
        "width": 0.64
    }

    wedges, _ = ax.pie(
        sizes,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops=wedgeprops,
        labels=None
    )

    for i, (wedge, cat, val) in enumerate(zip(wedges, categories, sizes)):
        theta1, theta2 = wedge.theta1, wedge.theta2
        angle_mid = math.radians((theta1 + theta2) / 2.0)

        label_r = 1.15
        lx = label_r * math.cos(angle_mid)
        ly = label_r * math.sin(angle_mid)

        ha = "left" if lx > 0.05 else ("right" if lx < -0.05 else "center")

        ax.text(
            lx, ly + 0.06, cat,
            color="#E5E5EA", fontsize=11, fontweight="600",
            ha=ha, va="center"
        )
        ax.text(
            lx, ly - 0.06, f"{val:.2f}%",
            color=colors[i], fontsize=13, fontweight="700",
            ha=ha, va="center"
        )

    inner_circle = plt.Circle((0, 0), 0.33, color="#0A0A0A", zorder=10)
    ax.add_patch(inner_circle)

    for wedge, name in zip(wedges, categories):
        cfg = LOGO_CONFIG[name]
        filename = LOCAL_LOGO_FILES[name]
        logo_path = os.path.join(images_dir, filename)

        theta1, theta2 = wedge.theta1, wedge.theta2
        angle_rad = math.radians((theta1 + theta2) / 2.0)

        r = cfg["radius"]
        x = r * math.cos(angle_rad)
        y = r * math.sin(angle_rad)

        if os.path.exists(logo_path):
            try:
                logo_img = load_image_asset(logo_path)
                max_w_h = cfg["max_size"]
                logo_img.thumbnail((max_w_h, max_w_h), Image.Resampling.LANCZOS)
                imagebox = OffsetImage(logo_img, zoom=1.0)
                ab = AnnotationBbox(
                    imagebox,
                    (x, y),
                    frameon=False,
                    pad=0.0,
                    zorder=12
                )
                ax.add_artist(ab)
            except Exception as e:
                logger.error(f"Erro ao inserir logo de {name} nas fatias do donut: {e}")
                _add_logo_fallback(ax, x, y, name, colors[categories.index(name)])
        else:
            _add_logo_fallback(ax, x, y, name, colors[categories.index(name)])

    ax.axis("equal")

    if save_path:
        try:
            fig.savefig(
                save_path,
                dpi=300,
                facecolor=BG_COLOR,
                bbox_inches="tight",
                pad_inches=0.08
            )
            logger.info(f"Gráfico donut de 5 fatias salvo com sucesso em: {save_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar imagem do donut: {e}")

    return fig, ax
