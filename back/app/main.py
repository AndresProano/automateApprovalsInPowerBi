from app.graph_extractor import get_access_token, get_approvals, resolve_user_id
from app.csv_transformer import to_csv
from app.sharepoint_uploader import upload_to_sharepoint
import os
from app.config import SITE_ID, DRIVE_ID, TARGET_USER_EMAIL, TARGET_USER_ID, FRONTEND_ORIGIN
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
def process(req: ApprovalResponse):
    email = resolve_user_id(req.id_token, get_access_token())
    token = get_access_token()
    user_id = TARGET_USER_ID
    user_id = TARGET_USER_ID
    lookup_email = TARGET_USER_EMAIL or email
    if not user_id:
        user_id = resolve_user_id(lookup_email, token)

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
