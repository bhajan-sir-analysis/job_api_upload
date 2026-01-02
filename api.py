from fastapi import FastAPI, File, UploadFile, Header, HTTPException
import csv
import io

app = FastAPI()

@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    authorization: str = Header(...)
):
    if authorization != "Bearer demo123":
        raise HTTPException(status_code=401, detail="Invalid token")

    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    rows = list(reader)

    return {
        "status": "success",
        "filename": file.filename,
        "total_rows": len(rows),
        "sample_row": rows[0] if rows else {}
    }

