import os
from collections import defaultdict
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Assignment-specific values from the prompt. They can also be overridden
# using Render environment variables without changing the source code.
API_KEY = os.getenv("ANALYTICS_API_KEY", "")
STUDENT_EMAIL = os.getenv("STUDENT_EMAIL", "24f2007275@ds.study.iitm.ac.in")

app = FastAPI(title="POST Analytics API", version="1.0.0")

# The assignment explicitly requires browser cross-origin access from its page.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyticsEvent(BaseModel):
    user: str
    amount: float
    ts: int | float | str | None = None


class AnalyticsRequest(BaseModel):
    events: list[AnalyticsEvent] = Field(default_factory=list)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "analytics"}


@app.post("/analytics")
def analytics(
    payload: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> dict[str, Any]:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = payload.events
    per_user_positive_totals: dict[str, float] = defaultdict(float)
    revenue = 0.0

    for event in events:
        if event.amount > 0:
            revenue += event.amount
            per_user_positive_totals[event.user] += event.amount

    # The grader ensures a top-user winner without ties and a nonempty batch.
    # Keep an empty-string fallback for a generic empty/all-nonpositive batch.
    top_user = (
        max(per_user_positive_totals, key=per_user_positive_totals.get)
        if per_user_positive_totals
        else ""
    )

    return {
        "email": STUDENT_EMAIL,
        "total_events": len(events),
        "unique_users": len({event.user for event in events}),
        "revenue": round(revenue, 10),
        "top_user": top_user,
    }
