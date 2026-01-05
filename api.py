from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
import os
import csv

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


# ✅ IMPORTANT: this must be OUTSIDE upload_csv
@app.get("/api/mapped-jobs")
def verify_mapped_jobs(limit: int = 5):
    file_path = "uploads/final_upload_ready.csv"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV file not found")

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    return {
        "status": "success",
        "total_records": len(rows),
        "sample_records": rows[:limit]
    }
@app.get("/view/mapped-jobs", response_class=HTMLResponse)
def view_mapped_jobs():
    file_path = "uploads/final_upload_ready.csv"

    if not os.path.exists(file_path):
        return "<h2>CSV file not found</h2>"

    rows = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    html = """
    <html>
    <head>
        <title>Mapped Jobs Preview</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            h2 { color: #333; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 8px; font-size: 14px; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #fafafa; }
        </style>
    </head>
    <body>
        <h2>Mapped Jobs Data</h2>
        <p><b>Total Records:</b> """ + str(len(rows)) + """</p>
        <table>
            <tr>
    """

    # Table headers
    for col in rows[0].keys():
        html += f"<th>{col}</th>"
    html += "</tr>"

    # Table rows
    for row in rows:
        html += "<tr>"
        for val in row.values():
            html += f"<td>{val}</td>"
        html += "</tr>"

    html += """
        </table>
    </body>
    </html>
    """

    return html




