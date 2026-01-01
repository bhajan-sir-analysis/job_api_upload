from fastapi import FastAPI, Header, UploadFile, File, HTTPException
from typing import List
import pandas as pd

app = FastAPI()

# -----------------------------
# JSON upload endpoint
# -----------------------------
@app.post("/upload")
def upload_jobs(
    data: List[dict],
    authorization: str = Header(...)
):
    if authorization != "Bearer demo123":
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "status": "success",
        "rows_received": len(data)
    }


# -----------------------------
# CSV upload endpoint
# -----------------------------
@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    authorization: str = Header(...)
):
    if authorization != "Bearer demo123":
        raise HTTPException(status_code=401, detail="Invalid token")

    df = pd.read_csv(file.file)

    return {
        "status": "success",
        "rows_received": len(df),
        "columns": list(df.columns)
    }

