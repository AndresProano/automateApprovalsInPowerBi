from graph_extractor import get_access_token, get_approvals, resolve_user_id, validate_id_token
from csv_transformer import to_csv
from sharepoint_uploader import upload_to_sharepoint
import os
from config import SITE_ID, DRIVE_ID, TARGET_USER_EMAIL, TARGET_USER_ID, FRONTEND_ORIGIN
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Approval Items Extractor", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ApprovalResponse(BaseModel):
    id_token: str

@app.post("/api/approvals/process")
def process(req: ProcessRequest):
    email = validate_id_token(req.id_token)
    token = get_access_token()
    user_id = TARGET_USER_ID
    if not user_id and TARGET_USER_EMAIL:
        user_id = resolve_user_id(TARGET_USER_EMAIL, token)
    approvals = get_approvals(token, user_id)
    csv_path = to_csv(approvals, "approvals.csv")

    # Ejecuta tu script adicional de organización
    os.system("python app/limpiezaDatos.py approvals.csv approvals_cleaned.csv")

    upload_to_sharepoint(
        token,
        "approvals.csv",
        SITE_ID,
        DRIVE_ID
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
