from fastapi import FastAPI, Header
import pandas as pd

app = FastAPI()

@app.post("/upload")
def upload_jobs(data: list, authorization: str = Header(None)):

    # 🔐 API KEY CHECK
    if authorization != "Bearer demo123":
        return {"status": "error", "message": "Unauthorized"}

    # Convert JSON → CSV
    df = pd.DataFrame(data)
    df.to_csv("received_data.csv", index=False)

    return {
        "status": "success",
        "rows_received": len(df)
    }
