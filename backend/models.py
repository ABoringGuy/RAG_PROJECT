from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

class SummaryResponse(BaseModel):
    answer: str

class PageRequest(BaseModel):
    start_page: int
    end_page: int
    query: str

class UploadResponse(BaseModel):
    message:str
    total_pages:int