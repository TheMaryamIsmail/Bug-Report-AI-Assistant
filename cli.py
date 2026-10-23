import os
from dotenv import load_dotenv
from graph import build_bug_analyzer_graph

load_dotenv()

def main():
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment variables. Check your .env file.")
        return

    # Sample input
    raw_bug_description = """
    When users click the Checkout button on mobile devices (iOS Safari), 
    the screen freezes and throws a 500 server error after 30 seconds. 
    It doesn't happen on desktop Chrome or Android devices. Money gets deducted from credit card 
    but no order confirmation email is sent or created in database.
    """

    print("🚀 Initializing AI Bug Report Analyzer Graph...")
    app = build_bug_analyzer_graph()

    initial_state = {
        "raw_bug_description": raw_bug_description,
    }

    print("\n⚡ Running LangGraph Nodes...")
    
    # Run the compiled graph through state streaming
    for step in app.stream(initial_state):
        node_name = list(step.keys())[0]
        print(f" -> Completed Node: [{node_name}]")

    # Get final state from invoke
    final_output = app.invoke(initial_state)

    print("\n" + "=" * 50)
    print("📋 FINAL STRUCTURED BUG REPORT")
    print("=" * 50 + "\n")
    print(final_output.get("formatted_report"))

if __name__ == "__main__":
    main()