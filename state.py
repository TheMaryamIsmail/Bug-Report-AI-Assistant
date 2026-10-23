from typing import TypedDict, Optional, List

class BugReportState(TypedDict):
    # Inputs
    raw_bug_description: str
    
    # Node 1 Outputs
    title: Optional[str]
    affected_feature: Optional[str]
    issue_summary: Optional[str]
    
    # Node 2 Outputs
    severity: Optional[str]  # Critical, High, Medium, Low
    severity_reasoning: Optional[str]
    
    # Node 3 Outputs
    root_cause_suggestions: Optional[List[str]]
    
    # Node 4 Outputs
    formatted_report: Optional[str]