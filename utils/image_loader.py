from io import BytesIO
from pathlib import Path

from PIL import Image

def load_image_asset(image_path):
    path = Path(image_path)
    if path.suffix.lower() == ".svg":
        try:
            import cairosvg
            png_bytes = cairosvg.svg2png(url=str(path))
            return Image.open(BytesIO(png_bytes)).convert("RGBA")
        except Exception:
            fallback_png = path.with_suffix(".png")
            if fallback_png.exists():
                return Image.open(fallback_png).convert("RGBA")
            raise RuntimeError(f"Unable to load SVG asset: {path}")
    return Image.open(path).convert("RGBA")
