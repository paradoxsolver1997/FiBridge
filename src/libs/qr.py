from PIL import Image
from typing import Optional
import qrcode

"""QR code utilities (refactored from generate_qr.py).

Provides a simple API to generate QR images, optionally embedding a rectangular logo.
"""


def generate_qr_image(url: str, qr_size: int = 600, logo_path: Optional[str] = None,
                                max_logo_ratio: float = 0.4) -> Image.Image:
    """Generate a QR code image from `url`. Optionally embed a rectangular logo.

    If `output_path` is provided the image will be saved to that path. The PIL Image is returned in all cases.
    """
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo_w, logo_h = logo.size
        scale_factor = min((qr_size * max_logo_ratio) / logo_w, (qr_size * max_logo_ratio) / logo_h)
        new_logo_size = (max(1, int(logo_w * scale_factor)), max(1, int(logo_h * scale_factor)))
        logo = logo.resize(new_logo_size, Image.Resampling.LANCZOS)
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
        qr_img.paste(logo, pos, mask=logo)

    return qr_img
