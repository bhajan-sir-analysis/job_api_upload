from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ✅ Security scheme
security = HTTPBearer()

class Job(BaseModel):
    job_title: str
    company: str
    location: str
    experience: str
    description: str

@app.post("/upload")
def upload_jobs(
    data: List[Job],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.credentials != "demo123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return {
        "status": "success",
        "rows_received": len(data)
    }


