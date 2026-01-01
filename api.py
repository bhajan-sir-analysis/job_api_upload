from fastapi import FastAPI, Header
from typing import List, Dict

app = FastAPI()

@app.post("/upload")
def upload_jobs(
    data: List[Dict],
    authorization: str = Header(None)
):
    if authorization != "Bearer demo123":
        return {"status": "error", "message": "Unauthorized"}

    return {
        "status": "success",
        "rows_received": len(data),
        "sample": data[:1]
    }
