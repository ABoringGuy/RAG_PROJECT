import faiss
from collections import defaultdict

def build_faiss_index(document_embeddings):
    dimension = document_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(document_embeddings)
    return index

section_index = defaultdict(list)
chunk_positions = {}

page_index = defaultdict(list)
page_positions = {}

def build_metadata_indexes(documents):
    section_index.clear()
    chunk_positions.clear()

    page_index.clear()
    page_positions.clear()
    for idx, doc in enumerate(documents):
        section_id= doc.metadata["section_id"]
        section_index[section_id].append(idx)

        page = doc.metadata["page"]
        page_index[page].append(idx)

    for chunk_list in section_index.values():
        chunk_list.sort()

        for position, chunk_idx in enumerate(chunk_list):
            chunk_positions[chunk_idx] = position
            page_positions[chunk_idx] = position

    return section_index, chunk_positions, page_index, page_positions