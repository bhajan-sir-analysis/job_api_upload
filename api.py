@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.credentials != "demo123":
        raise HTTPException(status_code=401, detail="Invalid token")

    content = await file.read()

    return {
        "status": "success",
        "filename": file.filename,
        "size": len(content)
    }






