import os
import sys
import logging
import threading
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from api.coingecko import get_global_data, get_stablecoin_market_cap
from utils.calculations import calculate_adjusted_dominance
from charts.pie_chart import generate_pie_chart, COLOR_BTC, COLOR_ETH, COLOR_STABLE, COLOR_ALT, COLOR_OTHERS
from utils.image_loader import load_image_asset

logger = logging.getLogger(__name__)

BG = "#000000"
SURFACE = "#111111"
DIVIDER = "#1D1D1F"
TEXT_PRI = "#F5F5F7"
TEXT_SEC = "#6E6E73"
ACCENT = "#0A84FF"

API_REFRESH_INTERVAL = 60


def get_images_dir():
    """Caminho absoluto robusto do diretório de imagens, funciona em dev e no .exe."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "images")
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        images_dir = os.path.abspath(os.path.join(exe_dir, "..", "images"))
        if not os.path.exists(images_dir):
            images_dir = os.path.join(exe_dir, "images")
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.abspath(os.path.join(current_dir, "images"))
    return images_dir


class CryptoDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gráfico de Dominância em Tempo Real")
        self.root.geometry("1400x820")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        self.dominance_data = None
        self.is_updating = False
        self.auto_refresh_job = None
        self.logo_tk_images = {}
        self.countdown_seconds = API_REFRESH_INTERVAL

        self._create_layout()
        self.trigger_refresh()
        self._schedule_tick()

    def _create_layout(self):
        """Constrói o layout de duas colunas Apple-style."""
        top = tk.Frame(self.root, bg=BG, height=72)
        top.pack(fill="x", padx=40, pady=(28, 0))
        top.pack_propagate(False)

        tk.Label(
            top, text="Dominância Cripto",
            font=("SF Pro Display", 26, "bold"),
            fg=TEXT_PRI, bg=BG
        ).pack(side="left", anchor="s", pady=(0, 4))

        tk.Frame(self.root, bg=DIVIDER, height=1).pack(side="top", fill="x", padx=40, pady=(12, 0))

        footer = tk.Frame(self.root, bg=BG, height=56)
        footer.pack(side="bottom", fill="x", padx=40, pady=(0, 0))
        footer.pack_propagate(False)

        tk.Frame(self.root, bg=DIVIDER, height=1).pack(side="bottom", fill="x", padx=40)

        body = tk.Frame(self.root, bg=BG)
        body.pack(side="top", fill="both", expand=True, padx=40, pady=20)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=0)
        body.columnconfigure(2, weight=0)
        body.rowconfigure(0, weight=1)

        self.chart_frame = tk.Frame(body, bg=BG)
        self.chart_frame.grid(row=0, column=0, sticky="nsew")

        self.loading_label = tk.Label(
            self.chart_frame,
            text="A obter dados do mercado…",
            font=("SF Pro Text", 13), fg=TEXT_SEC, bg=BG
        )
        self.loading_label.pack(expand=True)

        tk.Frame(body, bg=DIVIDER, width=1).grid(row=0, column=1, sticky="ns", padx=24)

        self.sidebar = tk.Frame(body, bg=BG, width=340)
        self.sidebar.grid(row=0, column=2, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.columnconfigure(0, weight=1)
        self.sidebar.rowconfigure(1, weight=1)

        tk.Label(
            self.sidebar,
            text="DOMINÂNCIA AJUSTADA",
            font=("SF Pro Text", 9, "bold"),
            fg=TEXT_SEC, bg=BG, anchor="w"
        ).grid(row=0, column=0, sticky="ew", pady=(8, 14))

        self.cards_container = tk.Frame(self.sidebar, bg=BG)
        self.cards_container.grid(row=1, column=0, sticky="nsew")
        self.cards_container.columnconfigure(0, weight=1)

        self.status_dot = tk.Label(footer, text="●", font=("SF Pro Text", 10),
                                   fg=TEXT_SEC, bg=BG)
        self.status_dot.pack(side="left", pady=16)

        self.status_label = tk.Label(
            footer, text="Inicializando…",
            font=("SF Pro Text", 10), fg=TEXT_SEC, bg=BG, anchor="w"
        )
        self.status_label.pack(side="left", padx=6, pady=16)

        self.refresh_button = tk.Button(
            footer,
            text="↻  Atualizar",
            command=self.trigger_refresh,
            font=("SF Pro Text", 10, "bold"),
            fg="#FFFFFF", bg=ACCENT,
            activebackground="#0066CC", activeforeground="#FFFFFF",
            relief="flat", padx=16, pady=6,
            cursor="hand2", bd=0
        )
        self.refresh_button.pack(side="right", pady=12)

    def trigger_refresh(self):
        if self.is_updating:
            return
        self.is_updating = True
        self.countdown_seconds = API_REFRESH_INTERVAL
        self._set_status("loading", "A sincronizar com a CoinGecko…")
        self.refresh_button.config(state="disabled", bg=DIVIDER, fg=TEXT_SEC)
        threading.Thread(target=self._fetch_thread, daemon=True).start()

    def _fetch_thread(self):
        try:
            global_data = get_global_data()
            stable_market_cap = get_stablecoin_market_cap()
            dominance_data = calculate_adjusted_dominance(global_data, stable_market_cap)
            self.root.after(0, self._update_ui, dominance_data)
        except Exception as e:
            logger.error(f"Erro na thread de atualização: {e}")
            self.root.after(0, self._handle_error, str(e))

    def _update_ui(self, dominance_data):
        self.dominance_data = dominance_data
        self.is_updating = False

        for child in self.chart_frame.winfo_children():
            child.destroy()

        fig, ax = generate_pie_chart(dominance_data, save_path=None)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        widget.configure(bg=BG)

        self._build_cards()

        now = datetime.now().strftime("%H:%M:%S")
        self._set_status("ok", f"Atualizado às {now}  ·  Próxima consulta em {self.countdown_seconds}s")
        self.refresh_button.config(state="normal", bg=ACCENT, fg="#FFFFFF")

    def _handle_error(self, error_msg):
        self.is_updating = False
        if self.dominance_data is None:
            fallback = {
                "Bitcoin": 54.00,
                "Ethereum": 17.00,
                "Stablecoins": 7.00,
                "Top 10 Alts": 15.00,
                "OTHERS": 7.00
            }
            self._update_ui(fallback)
            self._set_status("warn", "API limitada (429) — exibindo dados estimados")
        else:
            self._set_status("warn", f"Conexão instável — mantendo dados anteriores")
        self.refresh_button.config(state="normal", bg=ACCENT, fg="#FFFFFF")

    def _build_cards(self):
        for child in self.cards_container.winfo_children():
            child.destroy()

        assets = [
            ("Bitcoin",     "bitcoin.png",  COLOR_BTC,    "BTC · Líder de Mercado"),
            ("Ethereum",    "ethereum.png", COLOR_ETH,    "ETH · Smart Contracts"),
            ("Stablecoins", "tether.png",   COLOR_STABLE, "Stablecoins (USDT, etc.)"),
            ("Top 10 Alts", "doge.png",     COLOR_ALT,    "Top 10 Altcoins (BNB, SOL...)"),
            ("OTHERS",      "others.svg",   COLOR_OTHERS, "OTHERS.D (Cauda Longa)"),
        ]

        for row_idx, (name, img_file, color, desc) in enumerate(assets):
            value = self.dominance_data[name]
            self._make_card(name, img_file, color, desc, value, row=row_idx * 2)

            if row_idx < len(assets) - 1:
                sep = tk.Frame(self.cards_container, bg=DIVIDER, height=1)
                sep.grid(row=row_idx * 2 + 1, column=0, sticky="ew", pady=0)

    def _make_card(self, name, img_file, color, desc, value, row=0):
        card = tk.Frame(self.cards_container, bg=BG)
        card.grid(row=row, column=0, sticky="ew", pady=10)
        card.columnconfigure(1, weight=1)

        img_path = os.path.join(get_images_dir(), img_file)
        photo = None
        if os.path.exists(img_path):
            try:
                raw = load_image_asset(img_path)
                raw.thumbnail((36, 36), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(raw)
                self.logo_tk_images[name] = photo
            except Exception as e:
                logger.warning(f"Logo {name}: {e}")

        logo_lbl = tk.Label(card, bg=BG)
        if photo:
            logo_lbl.config(image=photo)
        else:
            logo_lbl.config(text="◉", font=("SF Pro Text", 18), fg=color)
        logo_lbl.grid(row=0, column=0, rowspan=2, padx=(0, 14), sticky="w")

        tk.Label(card, text=name,
                 font=("SF Pro Text", 14, "bold"),
                 fg=TEXT_PRI, bg=BG, anchor="w"
        ).grid(row=0, column=1, sticky="ew")

        tk.Label(card, text=desc,
                 font=("SF Pro Text", 9),
                 fg=TEXT_SEC, bg=BG, anchor="w"
        ).grid(row=1, column=1, sticky="ew")

        tk.Label(card,
                 text=f"{value:.2f}%",
                 font=("SF Pro Display", 22, "bold"),
                 fg=color, bg=BG
        ).grid(row=0, column=2, rowspan=2, padx=(12, 0), sticky="e")

    def _schedule_tick(self):
        self.auto_refresh_job = self.root.after(1000, self._tick)

    def _tick(self):
        if not self.is_updating:
            self.countdown_seconds -= 1
            if self.countdown_seconds <= 0:
                self.countdown_seconds = API_REFRESH_INTERVAL
                self.trigger_refresh()
            else:
                now = datetime.now().strftime("%H:%M:%S")
                self._set_status("ok",
                    f"Atualizado  ·  Próxima consulta em {self.countdown_seconds}s  ·  {now}")
        self._schedule_tick()

    def _set_status(self, state, text):
        colors = {"ok": "#30D158", "warn": "#FF9F0A", "loading": TEXT_SEC}
        self.status_dot.config(fg=colors.get(state, TEXT_SEC))
        self.status_label.config(text=text)


def start_gui():
    root = tk.Tk()
    CryptoDashboardApp(root)

    icon_path = os.path.join(get_images_dir(), "icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass

    root.mainloop()


if __name__ == "__main__":
    start_gui()
