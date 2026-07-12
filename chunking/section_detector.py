from chunking.parser_utils import get_body_font_size, heading_score, clean_text
import re


def detect_pdf_sections(pages):
    body_font_size, body_font_name=get_body_font_size(pages)
    #section_patterns = [r'^[A-Z][A-Z ]+$',
    #                    r'^#+\s+.+',
    #                    r'^.+\n[-=]{3,}$'
    #                    ]

    sections=[]
    section_id=0
    current_heading="Introduction"
    current_content=[]
    section_page=1
    heading_buffer=[]
    reading_heading=False
    previous_page=None

    for page in pages:
        current_page=page["page"]

        if(previous_page is not None
            and previous_page!=current_page
            and current_content):

            sections.append({
                "heading": current_heading,
                "section_id": section_id,
                "content": "\n".join(current_content).strip(),
                "page": previous_page
            })

        section_id += 1
        current_content = []
        section_page = current_page

        for block in page["text"]["blocks"]:
            # This ignores images
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                line_text=""

                for span in line["spans"]:
                    line_text+=span["text"]

                line_text=clean_text(line_text)


                if not line_text:
                    continue

                first_span= line["spans"][0]
                font_size=first_span["size"]



                score = heading_score(line_text,
                                      first_span,
                                      body_font_size,
                                      body_font_name)

                # print("=" * 60)
                # print("Detected heading:", line_text)
                # print("Score:", score)


                is_heading = score >= 4

                if is_heading and round(font_size):
                    if is_heading:
                        print("=" * 60)
                        print("Detected heading:", repr(line_text))
                        print("Score:", score)
                    reading_heading = True
                    heading_buffer.append(line_text)
                    continue

                if reading_heading:
                    if current_content:
                        sections.append({"heading": current_heading,
                                         "section_id":section_id,
                                         "content": "\n".join(current_content).strip(),
                                         "page": section_page})
                        section_id+=1

                    current_heading="\n".join(heading_buffer)
                    current_content=[]
                    section_page=current_page
                    heading_buffer=[]
                    reading_heading=False
                current_content.append(line_text)

        previous_page=current_page

    if reading_heading:
        current_heading = "\n".join(heading_buffer)
        current_content = [current_heading]

    if current_content:
        sections.append({"heading": current_heading,
                         "section_id":section_id,
                         "content": "\n".join(current_content).strip(),
                         "page": section_page})


    return sections