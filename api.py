from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ✅ Model
class Job(BaseModel):
    job_title: str
    company: str
    location: str
    experience: str
    description: str

@app.post("/upload")
def upload_jobs(
    data: List[Job],
    authorization: str = Header(None)
):
    if authorization != "Bearer demo123":
        return {"status": "error", "message": "Unauthorized"}

    return {
        "status": "success",
        "rows_received": len(data)
    }
