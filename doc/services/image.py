import gc

from paddleocr import PaddleOCR

_ocr = None


def get_ocr():
    global _ocr

    if _ocr is None:
        _ocr = PaddleOCR(
            lang="en",

            # Disable models you don't need
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

    return _ocr


def extract_image_text(image_path):

    ocr = get_ocr()

    result = ocr.predict(image_path)

    text = []

    for page in result:

        if "rec_texts" in page:
            text.extend(page["rec_texts"])

    gc.collect()

    return "\n".join(text)