from embedding.context_builder import build_context
from embedding.retrieval import retrieve_page_chunks, get_representative_chunks, retrieve_documents
from embedding.prompt_builder import build_prompt
from embedding.indexing import build_faiss_index, build_metadata_indexes
from embedding.embedding_model import embed_documents, embed_query
from embedding.groq_client import generate
from embedding.confidence import calculate_retrieval_confidence

def initialization(documents):
    total_pages= max(doc.metadata["page"] for doc in documents)
    document_embeddings= embed_documents(documents)
    index= build_faiss_index(document_embeddings)
    section_index, chunk_positions, page_index, page_positions = build_metadata_indexes(documents)
    return {
        "documents": documents,
        "index": index,
        "section_index": section_index,
        "chunk_positions": chunk_positions,
        "page_index": page_index,
        "total_pages": total_pages
    }

def generate_response(rag_data, mode, query="", start_page=None, end_page=None):
    documents = rag_data["documents"]
    index = rag_data["index"]
    section_index = rag_data["section_index"]
    chunk_positions = rag_data["chunk_positions"]
    page_index = rag_data["page_index"]
    #total_pages = rag_data["total_pages"] Delete later if not used

    if mode == "query":
        query_embedding = embed_query(query)

    if mode == "summary":
        include_pages = False

        retrieved_docs = get_representative_chunks(
            documents,
            section_index,
        )

    elif mode == "page":
        include_pages = False
        retrieved_docs = retrieve_page_chunks(
            start_page,
            end_page,
            page_index,
            documents,
        )

    else:
        include_pages = True
        scores, indices = index.search(
            query_embedding,
            k=8,
        )
        score=calculate_retrieval_confidence(scores)
        print("\nThe Confidence Scores is:",score,"\n")

        retrieved_docs = retrieve_documents(
            scores,
            indices,
            documents,
            section_index,
            chunk_positions,
        )

    context = build_context(retrieved_docs, include_pages)

    prompt = build_prompt(mode, context, query, start_page, end_page)
    #print(prompt[:1000])
    answer=generate(prompt)
    for i, doc in enumerate(retrieved_docs):
        print("=" * 80)
        print(doc.metadata["heading"])
        print(doc.metadata["page"])
        print(doc.metadata["section_id"])
        print(doc.page_content)
    # print("Length of Context is: ", len(context))

    return answer