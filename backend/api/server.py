from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.rag.engine import RAGEngine

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MedBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = RAGEngine()

class QueryRequest(BaseModel):
    text: str
    patient_id: Optional[str] = None

class UpdatePatientRequest(BaseModel):
    data: Dict[str, Any]

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MedBot API is running"}

@app.post("/query")
def query_agent(request: QueryRequest):
    response = rag_engine.query(request.text, request.patient_id)
    return {"response": response}

@app.post("/patient/{patient_id}/update")
def update_patient(patient_id: str, request: UpdatePatientRequest):
    result = rag_engine.update_patient(patient_id, request.data)
    return {"status": "success", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
