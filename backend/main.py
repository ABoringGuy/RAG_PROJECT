from fastapi import FastAPI, UploadFile, File
from backend.RAG_Pipeline import RAGPipeline
from backend.models import QueryRequest, QueryResponse, SummaryResponse,PageRequest
import shutil
import os

app = FastAPI()
pipeline = RAGPipeline()

@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    upload_path = os.path.join("uploads", file.filename)

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    metadata = pipeline.load_document(upload_path)

    return {
        "message": "Document uploaded successfully.",
        "total_pages": metadata["total_pages"]
            }

@app.post("/query", response_model=QueryResponse)
def query_document(request: QueryRequest):
    answer = pipeline.query(request.query)
    return {"answer": answer}

@app.post("/summary", response_model=SummaryResponse)
def generate_summary():
    answer=pipeline.summarize()
    return {"answer": answer}

@app.post("/page")
def retrieve_page(request: PageRequest):
    answer = pipeline.page_query(request.start_page, request.end_page, request.query)
    return {"answer": answer}

