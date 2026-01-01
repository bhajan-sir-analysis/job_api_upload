from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import pandas as pd

app = FastAPI()

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

