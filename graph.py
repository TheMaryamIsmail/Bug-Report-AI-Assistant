from langgraph.graph import StateGraph, START, END
from state import BugReportState
from nodes import (
    analyze_bug,
    detect_severity,
    suggest_root_causes,
    format_report,
)

def build_bug_analyzer_graph():
    workflow = StateGraph(BugReportState)

    # Add Nodes
    workflow.add_node("analyze_bug", analyze_bug)
    workflow.add_node("detect_severity", detect_severity)
    workflow.add_node("suggest_root_causes", suggest_root_causes)
    workflow.add_node("format_report", format_report)

    # Define Sequential Edges
    workflow.add_edge(START, "analyze_bug")
    workflow.add_edge("analyze_bug", "detect_severity")
    workflow.add_edge("detect_severity", "suggest_root_causes")
    workflow.add_edge("suggest_root_causes", "format_report")
    workflow.add_edge("format_report", END)

    return workflow.compile()