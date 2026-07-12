from collections import Counter
import re
import math

def heading_score(line, first_span, body_font_size, body_font_name):
    score = 0
    text = clean_text(line)

    font_size = round(first_span["size"])
    font_name = first_span["font"]
    has_letters = re.search(r"[A-Za-z]", text) is not None


    if not text:
        return 0


    if font_size > body_font_size:
        score +=3

    if font_name != body_font_name and not "bold" in font_name:
        score += 2

    if "bold" in font_name:
        score += 2

    # Matches terms like:
    # 1 INTRODUCTION
    # 1.INTRODUCTION
    # 1) INTRODUCTION
    # 1.1 BACKGROUND
    # 1.1.BACKGROUND
    # I INTRODUCTION
    # I.INTRODUCTION
    # I) INTRODUCTION
    # II.RELATED WORK
    if re.fullmatch(r"((\d+(\.\d+)*)|([IVXLC]+|[A-Z]))?[\.\)]?\s+[A-Z][A-Za-z0-9 ()/&\-:]+", text):
        score += 3
    elif re.match(r'^[A-Z][A-Z ]+$', text):
        score += 2

    # If Heading is Underlined
    if re.match(r"^.+\n[-=]{3,}$", text):
        score += 3

    if len(text.split()) <=10:
        score += 1

    if len(text.split()) > 20:
        score -= 3

    # To prevent Equations
    if "=" in text:
        score -= 2

    # Heading rarely end with Full stops and other Punctuations
    if re.search(r"[.,;]$", text):
        score -= 2
    # Lower penalty because ? and ! can be used on main heading(but less common)
    if re.search(r"[?!]$", text):
        score -= 1
    # Detect Bullet Points
    if re.match(r'^\s*[•\-*]\s+', text):
        score -= 1

    if not has_letters:
        score -= 3

    if font_name == "OCR" and font_size ==1:
        score -= 5
    return score



def get_body_font_size(pages):
    """
    Determines the document's body font size by sampling text and
    weighting each font size by the number of non-whitespace characters.
    """

    font_size_counter = Counter()
    font_name_counter = Counter()
    chars_read = 0

    # Dynamic sampling target based on document size
    num_pages = len(pages)
    target_chars = int(3000 + 2500 * math.log2(num_pages + 1))

    for page in pages:
        for block in page["text"]["blocks"]:

            if block["type"] != 0:
                continue

            for line in block["lines"]:

                if not line["spans"]:
                    continue

                # Build line text
                line_text = ""

                for span in line["spans"]:
                    line_text += span["text"]

                line_text = clean_text(line_text)

                if not line_text:
                    continue

                # Use first span's font size
                font_size = round(line["spans"][0]["size"])
                font_name = line["spans"][0]["font"]
                # Weight = number of non-whitespace characters
                weight = len(re.sub(r"\s+", "", line_text))

                font_size_counter[font_size] += weight
                font_name_counter[font_name] += weight
                chars_read += weight

                if chars_read >= target_chars:
                    return font_size_counter.most_common(1)[0][0], font_name_counter.most_common(1)[0][0]

    # Fallback for short documents
    return font_size_counter.most_common(1)[0][0], font_name_counter.most_common(1)[0][0]

def clean_text(text):
    # remove excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(
        r'\.{5,}\s*(\d+|[ivxlcdmIVXLCDM]+)\s*$',
        r' ... \1',
        text
    )
    return text.strip()