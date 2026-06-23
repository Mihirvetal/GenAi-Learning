from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware  # <-- IMPORT THIS
from pydantic import BaseModel
import os
from src.ingestion import run_ingestion
from src.rag_pipeline import query_rag

app = FastAPI(title="End-to-End Modular RAG Platform")

# ----------------- ADD CORS MIDDLEWARE HERE -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (like your local HTML file)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)
# ------------------------------------------------------------

class QueryRequest(BaseModel):
    question: str

class IngestRequest(BaseModel):
    file_name: str

@app.get("/")
def read_root():
    return {"status": "online", "engine": "Haystack 2.0 + Pinecone + Mistral"}

@app.post("/query")
def ask_question(request: QueryRequest):
    try:
        answer = query_rag(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        print(f"\n❌ PIPELINE CRASHED: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def ingest_file(request: IngestRequest, background_tasks: BackgroundTasks):
    file_path = os.path.join("data", request.file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found in data/ directory: {request.file_name}")
    
    background_tasks.add_task(run_ingestion, file_path)
    return {"message": f"Ingestion pipeline started in background for {request.file_name}"}