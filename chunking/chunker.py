from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


splitter= RecursiveCharacterTextSplitter(chunk_size=700,
                                         chunk_overlap=70,
                                         separators=["\n\n", "\n", ". ", " ", ""])

def chunk_sections(sections):
    chunks=[]
    chunk_id=0

    for section in sections:
        split_text=splitter.split_text(section["content"])

        for text in split_text:
            text = f"Heading: {section['heading']}\n\nPage Number:{section["page"]}\n\ntext:{text}"
            chunks.append({"text":text,
                           "heading": section["heading"],
                           "page": section["page"],
                           "chunk_id": chunk_id,
                           "section_id": section["section_id"]})

            chunk_id+=1
    return chunks

def create_documents(chunks):
    documents=[]
    for chunk in chunks:
        documents.append(
            Document(
                page_content=chunk["text"],
                metadata={"heading": chunk["heading"],
                          "page": chunk["page"],
                          "chunk_id": chunk["chunk_id"],
                          "section_id":chunk["section_id"]
                          }
            )
        )
    return documents