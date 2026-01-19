import shutil
from pathlib import Path
from subprocess import PIPE, CalledProcessError, run

from fitz import Matrix, csCMYK
from fitz import open as fitzopen
from PIL import Image


def convert_pdf_to_cmyk_tiff_custom(
    pdf_path: Path,
    output_path: Path,
    resolution: int = 500,
    icc_profile_path: Path | None = None,
) -> None:
    """
    Convert a CMYK PDF to a multi‑page CMYK TIFF **without** going through an RGB stage.

    Parameters
    ----------
    pdf_path : pathlib.Path
        Path to the input PDF.
    output_path : pathlib.Path
        Destination for the TIFF.
    resolution : int, default 500
        DPI at which each page is rendered.
    icc_profile_path : pathlib.Path, optional
        Path to a CMYK ICC profile that will be embedded in the TIFF.
    """
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # ------------------------------------------------------------------
    # 1. Open the PDF with PyMuPDF
    # ------------------------------------------------------------------
    doc = fitzopen(str(pdf_path))
    if doc.page_count == 0:
        raise ValueError("PDF contains no pages")

    # ------------------------------------------------------------------
    # 2. Render the page - we assume there is only one page
    # ------------------------------------------------------------------
    page = doc[0]
    pix = page.get_pixmap(
        matrix=Matrix(resolution / 72, resolution / 72),
        colorspace=csCMYK,
    )
    # Convert the raw CMYK data to a Pillow Image
    img_cmyk = Image.frombytes(
        "CMYK",
        (pix.width, pix.height),
        pix.samples,
        "raw",
        "CMYK",
        0,
        1,
    )

    doc.close()
    del page, pix, doc
    # ------------------------------------------------------------------
    # 3. Save as a multi‑page TIFF, embedding the ICC profile if supplied
    # ------------------------------------------------------------------
    try:
        save_kwargs = {
            "format": "TIFF",
            "compression": "tiff_lzw",
            "save_all": True,
            "dpi": (resolution, resolution),
        }
        if icc_profile_path and icc_profile_path.is_file():
            save_kwargs["icc_profile"] = icc_profile_path.read_bytes()

        img_cmyk.save(str(output_path), **save_kwargs)
    except Exception as exc:
        raise RuntimeError(f"Failed to write TIFF: {exc}") from exc


def convert_pdf_to_cmyk_tiff_gs(pdf_path: Path, output_path: Path):
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    gs_cmd = shutil.which("gs") or shutil.which("gswin64c")
    if not gs_cmd:
        raise EnvironmentError("Ghostscript is not installed or not in PATH")

    # Confirm Ghostscript version
    gs_check = run([gs_cmd, "--version"], capture_output=True, text=True)
    if gs_check.returncode != 0:
        raise EnvironmentError("Ghostscript not working correctly")

    # Check available devices
    devices_check = run([gs_cmd, "-h"], capture_output=True, text=True)
    gs_device = "tiff32nc" if "tiff32nc" in devices_check.stdout else "tiffsep"

    gs_command = [
        gs_cmd,
        "-dSAFER",
        "-dBATCH",
        "-dNOPAUSE",
        "-dNOPROMPT",
        f"-sDEVICE={gs_device}",  # tiff32nc or tiffsep
        "-sCompression=lzw",
        "-sColorConversionStrategy=LeaveColorUnchanged",
        "-dUseCIEColor",
        "-r500",  # <<< SET RESOLUTION HERE
        "-dGraphicsAlphaBits=4",  # Improve pattern raster
        "-dTextAlphaBits=4",  # Improve text smoothing
        f"-sOutputFile={str(output_path)}",
        str(pdf_path),
    ]

    _ = run(gs_command, capture_output=True, text=True)
