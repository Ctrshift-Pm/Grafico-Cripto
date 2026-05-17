import sys
import logging
from gui import start_gui

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Iniciando Dashboard de Dominância Cripto (GUI)...")
    try:
        start_gui()
    except Exception as e:
        logger.critical(f"Erro fatal na interface gráfica: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
