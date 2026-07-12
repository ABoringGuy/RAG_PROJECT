from chunking.parser_utils import get_body_font_size
from chunking.chunker import chunk_sections,create_documents
from chunking.section_detector import detect_pdf_sections
from chunking.parser_selector import parse_document
import pymupdf

def parse_pdf(path):
    doc= pymupdf.open(path)
    pages=[]

    for page_no, page in enumerate(doc):
        pages.append({"page": page_no+1,
                      "text": page.get_text("dict")})
    return pages

def process_document(file_path):
    #pages= parse_pdf(file_path)
    pages=parse_document(file_path)
    body_font_size,_ = get_body_font_size(pages)
    print(f"Detected body font size: {body_font_size}")
    sections=detect_pdf_sections(pages)
    chunks=chunk_sections(sections)
    documents=create_documents(chunks)

    print(chunks)
    #print(documents.heading)

    return documents


# page_content = chunk["text"],
# metadata = {"heading": chunk["heading"],
#             "page": chunk["page"],
#             "chunk_id": chunk["chunk_id"],
#             "section_id": chunk["section_id"]
#             }

