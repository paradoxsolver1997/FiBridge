
from tkinter import filedialog
import tempfile
import os
from src.lib import converter
from PIL import Image

def save_image_as_vector(img: Image.Image):
    """
    Save PIL image as vector format file (SVG/PDF/EPS/PS), auto popup save dialog.
    img: PIL.Image object (cropped/processed)
    output_dir: default save directory
    log_func: optional log function
    """

    tmp_dir = tempfile.gettempdir()
    tmp_bmp = os.path.join(tmp_dir, f'tmp_sig_{os.getpid()}.bmp')
    img.convert('L').save(tmp_bmp, format='BMP')
    filetypes = [
        ("SVG files", "*.svg"),
        ("PDF files", "*.pdf"),
        ("EPS files", "*.eps"),
        ("PS files", "*.ps"),
        ("All supported", "*.svg;*.pdf;*.eps;*.ps")
    ]
    filepath = filedialog.asksaveasfilename(
        defaultextension=".svg",
        filetypes=filetypes
    )
    if filepath:
        ext = os.path.splitext(filepath)[1].lower().lstrip('.')
        if ext not in ("svg", "pdf", "eps", "ps"):
            ext = 'svg'
        converter.bmp_to_vector(tmp_bmp, filepath)
    try:
        os.remove(tmp_bmp)
    except Exception:
        pass

    return filepath, ext


def save_image_as_bitmap(img: Image.Image, transparent: bool = False):
    filetypes = [
        ("PNG files", "*.png"),
        ("JPEG files", "*.jpg;*.jpeg"),
        ("BMP files", "*.bmp"),
        ("TIFF files", "*.tif;*.tiff"),
        ("All supported", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff")
    ]
    filepath = filedialog.asksaveasfilename(
        defaultextension=".png", 
        filetypes=filetypes
    )
    ext = os.path.splitext(filepath)[1].lower() if filepath else ''
    if filepath:
        if not transparent:
            img = img.convert("RGB")  # Discard alpha, background becomes white
        img.save(filepath)
    return filepath, ext