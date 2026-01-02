from fastapi import FastAPI, File, UploadFile, Header, HTTPException
import pandas as pd
import io
import os
from datetime import datetime

app = FastAPI()

API_KEY = "demo123"

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    authorization: str = Header(...)
):
    # 🔐 Auth check
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid token")

    # 📥 Read CSV
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode()))

    # ✅ CLEANING LOGIC
    required_cols = ["job_title", "company", "location"]

    for col in required_cols:
        if col not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing column: {col}"
            )

    df = df.dropna(subset=required_cols)
    df = df.drop_duplicates()

    # 💾 Save cleaned file
    filename = f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(output_path, index=False)

    return {
        "status": "success",
        "rows_received": len(df),
        "file_saved": filename
    }








