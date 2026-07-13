from chunking.parser_utils import get_body_font_size
from chunking.chunker import chunk_sections,create_documents
from chunking.section_detector import detect_pdf_sections
from chunking.parser_selector import parse_document

def process_document(file_path):
    pages=parse_document(file_path)
    body_font_size,_ = get_body_font_size(pages)
    print(f"Detected body font size: {body_font_size}")
    sections=detect_pdf_sections(pages)
    chunks=chunk_sections(sections)
    documents=create_documents(chunks)
    return documents

