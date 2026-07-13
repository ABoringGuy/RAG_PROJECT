import io
import pymupdf
import pytesseract
from PIL import Image
import shutil
import os
from dotenv import load_dotenv

load_dotenv()
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

tesseract_cmd = os.getenv("TESSERACT_CMD")

if tesseract_cmd and os.path.exists(tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
elif shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")
else:
    raise RuntimeError("Tesseract executable not found.")

def extract_image_text(page, bbox):
    rect = pymupdf.Rect(bbox)
    pix = page.get_pixmap(
        clip=rect,
        dpi=300
    )
    image = Image.open(io.BytesIO(pix.tobytes("png")))

    try:
        text = pytesseract.image_to_string(image)
    except Exception as e:
        print("OCR Error:", e)
        return None

    text = text.strip()

    # Ignore images with little/no readable text
    if len(text.split()) < 3:
        return None
    return text


def create_ocr_block(text, bbox):
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        lines.append({
            "spans": [
                {
                    "text": line,
                    "size": 1,#Size 1 so that it is never detected as heading(Headings usually need to be greater than normal body font size)
                    "font": "OCR"
                }
            ]
        })

    if not lines:
        return None

    return {
        "type": 0,
        "bbox": bbox,
        "lines": lines
    }


def parse_pdf(path):
    doc = pymupdf.open(path)
    pages = []
    print(type(doc))

    for page_no, page in enumerate(doc):
        text_dict = page.get_text("dict")
        new_blocks = []

        for block in text_dict["blocks"]:
            if block["type"] == 0:
                new_blocks.append(block)


            elif block["type"] == 1:# Type 1 is image blocks
                ocr_text = extract_image_text(
                    page,
                    block["bbox"]
                )

                if not ocr_text:
                    continue

                ocr_block = create_ocr_block(ocr_text,
                                             block["bbox"])

                if ocr_block:
                    new_blocks.append(ocr_block)

        text_dict["blocks"] = new_blocks

        pages.append({
            "page": page_no + 1,
            "text": text_dict
        })
    doc.close()
    return pages