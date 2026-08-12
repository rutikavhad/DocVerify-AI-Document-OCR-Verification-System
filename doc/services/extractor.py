from pathlib import Path

from .image import extract_image_text
from .pdf import extract_pdf_text


IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
}


def extract_document(path):

    ext = Path(path).suffix.lower()

    if ext == ".pdf":
        return extract_pdf_text(path)

    if ext in IMAGE_EXTENSIONS:
        return extract_image_text(path)

    raise ValueError(f"Unsupported file type: {ext}")