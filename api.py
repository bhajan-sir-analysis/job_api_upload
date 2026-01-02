from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from typing import Optional

app = FastAPI()

@app.post("/upload-csv")
def upload_csv(
    file: UploadFile = File(...),
    authorization: Optional[str] = Header(None)
):
    if authorization != "Bearer demo123":
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "status": "success",
        "filename": file.filename
    }

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


