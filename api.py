from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ✅ Swagger Authorization enable
security = HTTPBearer()

# ---------- MODEL ----------
class Job(BaseModel):
    job_title: str
    company: str
    location: str
    experience: str
    description: str

# ---------- API ----------
@app.post("/upload")
def upload_jobs(
    data: List[Job],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Token check
    if credentials.credentials != "demo123":
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "status": "success",
        "rows_received": len(data)
    }


