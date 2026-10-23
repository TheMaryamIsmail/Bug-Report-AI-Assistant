from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from graph import build_bug_analyzer_graph

load_dotenv()

app = FastAPI(
    title="AI Bug Report Analyzer API",
    description="LangGraph workflow powered by Gemini for analyzing software bug reports.",
    version="1.0.0"
)

# Setup Jinja2 templates folder
templates = Jinja2Templates(directory="templates")

bug_graph_app = build_bug_analyzer_graph()

class BugRequest(BaseModel):
    bug_description: str


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/analyze-bug/")
def analyze_bug_endpoint(request: BugRequest):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured.")
    
    if not request.bug_description.strip():
        raise HTTPException(status_code=400, detail="bug_description cannot be empty.")

    try:
        initial_state = {
            "raw_bug_description": request.bug_description
        }
        
        final_state = bug_graph_app.invoke(initial_state)
        
        return {
            "title": final_state.get("title"),
            "affected_feature": final_state.get("affected_feature"),
            "issue_summary": final_state.get("issue_summary"),
            "severity": final_state.get("severity"),
            "severity_reasoning": final_state.get("severity_reasoning"),
            "root_cause_suggestions": final_state.get("root_cause_suggestions"),
            "formatted_report": final_state.get("formatted_report")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))