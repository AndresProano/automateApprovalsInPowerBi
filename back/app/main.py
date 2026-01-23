2
import subprocess
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import (
    FRONTEND_ORIGIN,
    TARGET_USER_ID,
    OUTPUT_FILENAME,
    CLEAN_OUTPUT_FILENAME,
)
from app.graph_extractor import (
    fetch_approvals_from_graph
)
from app.csv_transformer import to_csv
from app.sharepoint_uploader import upload_to_sharepoint
from app.limpiarSimplificado import clean as clean_csv

app = FastAPI(title="Approval Items Extractor", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/approvals")

def get_data(authorization: str = Header(None), user_id: Optional[str]=None):
    if not authorization: 
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    try:

        print("Token recibido:", token)
        approvals = fetch_approvals_from_graph(token)

        if not approvals:
            return {"ok": True, "count": 0, "items": [], "message": "No items found"}
        
        to_csv(approvals, OUTPUT_FILENAME)

        clean_csv(OUTPUT_FILENAME, CLEAN_OUTPUT_FILENAME)

        upload_to_sharepoint(CLEAN_OUTPUT_FILENAME)

        return{
            "ok": True,
            "count": len(approvals),
            "items": approvals,
            "message": "Process completed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    