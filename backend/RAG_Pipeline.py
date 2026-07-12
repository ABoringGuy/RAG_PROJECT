from chunking.chunker_main import process_document
from embedding.embedding_main import initialization, generate_response


class RAGPipeline:
    def __init__(self):
        self.rag = None

    def ensure_loaded(self):
        if self.rag is None:
            raise RuntimeError("No document has been loaded.")

    def load_document(self, path):
        documents = process_document(path)
        self.rag = initialization(documents)
        return {"total_pages": self.rag["total_pages"]}

    def query(self, question):
        self.ensure_loaded()
        return generate_response(self.rag, mode="query", query=question)

    def summarize(self):
        self.ensure_loaded()
        return generate_response(self.rag, mode="summary")

    def page_query(self, start_page, end_page, question=""):
        self.ensure_loaded()
        return generate_response(self.rag, mode="page", query=question, start_page=start_page, end_page=end_page)

