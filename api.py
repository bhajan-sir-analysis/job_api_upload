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
# -----------------------------
# JSON upload endpoint
# -----------------------------
@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    authorization: str = Header(None)
):
    # 🔐 Authorization check
    if authorization != "Bearer demo123":
        raise HTTPException(status_code=401, detail="Invalid token")

    # ✅ CSV read
    df = pd.read_csv(file.file)

    # (Optional) Save file
    df.to_csv("received_jobs.csv", index=False)

    return {
        "status": "success",
        "rows_received": len(df),
        "columns": list(df.columns)
    }


