from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

from app.services.agent_service import (
    investigate_incident,
    record_resolution,
)


app = FastAPI(
    title="IncidentMind",
    description="AI incident-response agent with long-term memory.",
    version="1.0.0",
)


class IncidentRequest(BaseModel):
    incident_id: str
    service: str
    severity: str
    incident: str
    reported_at: str | None = None


class ResolutionRequest(BaseModel):
    incident_id: str
    service: str
    severity: str
    incident: str
    resolution: str
    successful: bool
    engineer_note: str = ""
    reported_at: str | None = None


@app.get("/")
def root():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "hindsight": "connected",
        "groq": "configured",
    }


@app.post("/investigate")
def investigate(request: IncidentRequest):

    reported_at = request.reported_at

    if not reported_at:
        reported_at = datetime.now(timezone.utc).isoformat()

    return investigate_incident(
        incident=request.incident,
        incident_id=request.incident_id,
        service=request.service,
        severity=request.severity,
        reported_at=reported_at,
    )


@app.post("/resolve")
def resolve(request: ResolutionRequest):

    reported_at = request.reported_at

    if not reported_at:
        reported_at = datetime.now(timezone.utc).isoformat()

    return record_resolution(
        incident=request.incident,
        incident_id=request.incident_id,
        service=request.service,
        severity=request.severity,
        resolution=request.resolution,
        successful=request.successful,
        engineer_note=request.engineer_note,
        reported_at=reported_at,
    )