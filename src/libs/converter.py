"""Bitmap conversion utilities.

Uses Pillow for most bitmap format conversions and pillow-heif for HEIC/HEIF decoding.
"""
from PIL import Image
import os
import subprocess
from typing import Optional, Callable
import tempfile
import shutil
import json
import importlib


def bmp_to_vector(
    in_path: str, 
    out_path: str, 
    log_fun: Optional[Callable[[str], None]] = None
) -> None:
    """
    Convert BMP bitmap to vector graphics (eps/svg/pdf/ps) using potrace.exe.
    Only supports grayscale or black-and-white BMP.
    out_fmt: eps/svg/pdf/ps
    """
    out_fmt = os.path.splitext(out_path)[1].lower().lstrip('.')
    potrace_exe = None
    if check_tool('potrace'):
        potrace_exe = shutil.which('potrace')
    if not potrace_exe:
        raise RuntimeError('potrace.exe not found in PATH; please install and configure the environment variable')

    if out_fmt not in ['eps', 'svg', 'pdf', 'ps']:
        raise RuntimeError(f'Unsupported output format for potrace: {out_fmt}')
    # potrace only supports BMP input

    ext = os.path.splitext(in_path)[1].lower()
    if ext != '.bmp':
        # Automatically convert to bmp temporary file
        with Image.open(in_path) as im:
            tmp_dir = tempfile.gettempdir()
            tmp_bmp = os.path.join(tmp_dir, f'tmp_potrace_{os.getpid()}.bmp')
            im.convert('L').save(tmp_bmp, format='BMP')
            in_path = tmp_bmp
    cmd = [potrace_exe, in_path, '-o', out_path, '-b', out_fmt.lower()]
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        raise RuntimeError(f'potrace.exe failed: {e}')


def check_tool(tool_key: str) -> bool:
    # DLL detection
    if tool_key.lower().endswith('.dll'):
        for p in os.environ.get('PATH', '').split(os.pathsep):
            if os.path.exists(os.path.join(p, tool_key)):
                return True
        return False
    """
    Check if a single tool is available, returning True/False.
    """
    
    tool_list_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'configs', 'tool_list.json')
    with open(tool_list_path, 'r', encoding='utf-8') as f:
        tool_list = json.load(f)
    tool = next((t for t in tool_list if t["key"] == tool_key), None)
    if tool:
        if tool["type"] == "exe" and tool["executables"]:
            exe_path = None
            for exe_name in tool["executables"]:
                exe_path = shutil.which(exe_name)
                if exe_path:
                    break
            if not exe_path:
                return False
            # Optional: further validation (e.g. ghostscript --version)
            if tool["key"] == "ghostscript":
                try:
                    proc = subprocess.run([exe_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
                    if proc.returncode == 0:
                        return True
                except Exception:
                    try:
                        proc = subprocess.run([exe_path, '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
                        if proc.returncode == 0:
                            return True
                    except Exception:
                        return False
                return False
            else:
                return True
        elif tool["type"] == "python" and tool["key"] == "cairosvg":
            return importlib.util.find_spec('cairosvg') is not None
        else:
            return False
    # If tool_list.json does not define the key, try to detect it as a python package
    try:
        return importlib.util.find_spec(tool_key) is not None
    except Exception:
        return False

