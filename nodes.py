import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError
from state import BugReportState

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ Error: GEMINI_API_KEY is missing from your environment variables or .env file.")

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3.8-flash"


# Pydantic Schemas for Structured Output
class BugAnalysisSchema(BaseModel):
    title: str = Field(description="A concise 5-8 word title for the bug")
    affected_feature: str = Field(description="The component or feature impacted")
    issue_summary: str = Field(description="A clear 2-3 sentence summary of the issue")


class SeveritySchema(BaseModel):
    severity: str = Field(description="One of: Critical, High, Medium, or Low")
    reasoning: str = Field(description="Brief rationale for assigning this severity rating")


class RootCauseSchema(BaseModel):
    possible_root_causes: list[str] = Field(description="2-4 technical suggestions for the root cause")


# Reusable decorator to automatically retry on 503/Server errors
ai_retry = retry(
    retry=retry_if_exception_type(ServerError),
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)


# ---------------------------------------------------------------------------
# Node 1: Bug Analysis
# ---------------------------------------------------------------------------
@ai_retry
def analyze_bug(state: BugReportState) -> dict:
    prompt = f"Analyze the following bug description and extract the key information.\n\nBug Description:\n{state['raw_bug_description']}"
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=BugAnalysisSchema,
            temperature=0.2,
        ),
    )
    data = BugAnalysisSchema.model_validate_json(response.text)
    return {
        "title": data.title,
        "affected_feature": data.affected_feature,
        "issue_summary": data.issue_summary,
    }


# ---------------------------------------------------------------------------
# Node 2: Severity Detection
# ---------------------------------------------------------------------------
@ai_retry
def detect_severity(state: BugReportState) -> dict:
    prompt = f"Classify the severity of this software bug as Critical, High, Medium, or Low.\n\nTitle: {state['title']}\nFeature: {state['affected_feature']}\nSummary: {state['issue_summary']}\nOriginal Report: {state['raw_bug_description']}"
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SeveritySchema,
            temperature=0.1,
        ),
    )
    data = SeveritySchema.model_validate_json(response.text)
    return {
        "severity": data.severity,
        "severity_reasoning": data.reasoning,
    }


# ---------------------------------------------------------------------------
# Node 3: Root Cause Suggestion
# ---------------------------------------------------------------------------
@ai_retry
def suggest_root_causes(state: BugReportState) -> dict:
    prompt = f"Suggest technical root causes for the following issue.\n\nTitle: {state['title']}\nFeature: {state['affected_feature']}\nSummary: {state['issue_summary']}\nOriginal Input: {state['raw_bug_description']}"
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RootCauseSchema,
            temperature=0.3,
        ),
    )
    data = RootCauseSchema.model_validate_json(response.text)
    return {
        "root_cause_suggestions": data.possible_root_causes,
    }


# ---------------------------------------------------------------------------
# Node 4: Format Report
# ---------------------------------------------------------------------------
@ai_retry
def format_report(state: BugReportState) -> dict:
    causes_str = "\n".join([f"- {cause}" for cause in state['root_cause_suggestions']])
    prompt = f"Format the following analyzed bug data into a clean, markdown-formatted bug report.\n\nTitle: {state['title']}\nSeverity: {state['severity']} (Reasoning: {state['severity_reasoning']})\nAffected Feature: {state['affected_feature']}\nIssue Summary: {state['issue_summary']}\nRoot Cause Suggestions:\n{causes_str}\nRaw Description: {state['raw_bug_description']}\n\nProvide a professional, clean Markdown report ready for Jira or GitHub Issues."
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2),
    )
    return {
        "formatted_report": response.text,
    }