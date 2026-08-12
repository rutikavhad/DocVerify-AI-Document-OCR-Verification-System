import gc
import os
import tempfile

import fitz

from .image import extract_image_text


def extract_pdf_text(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    try:

        # Try extracting searchable text first
        for page in doc:
            text += page.get_text()

        # If searchable text exists, return it
        if len(text.strip()) > 20:
            return text

        # Otherwise OCR the scanned pages
        text = ""

        for page in doc:

            # 150 DPI is usually enough and uses much less RAM than 300 DPI
            pix = page.get_pixmap(dpi=150)

            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False,
            ) as tmp:

                image_path = tmp.name

            pix.save(image_path)

            try:
                text += extract_image_text(image_path)
                text += "\n"

            finally:

                if os.path.exists(image_path):
                    os.remove(image_path)

            # Free page memory
            del pix
            gc.collect()

        return text

    finally:

        doc.close()
        gc.collect()