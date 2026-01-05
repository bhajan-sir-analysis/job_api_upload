from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

app = FastAPI()
security = HTTPBearer()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.credentials != "demo123":
        raise HTTPException(status_code=401, detail="Invalid token")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "status": "success",
        "saved_path": file_path
    }
