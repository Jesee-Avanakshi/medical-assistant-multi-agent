from langgraph.graph import StateGraph, END
from backend.state import MedicalState

from backend.agents.analyzer import analyze_medical_report
from backend.agents.recommender import recommend_doctors
from backend.agents.booking import book_appointment
from backend.agents.emailer import send_email

graph = StateGraph(MedicalState)

# ---------------- Nodes ----------------
graph.add_node("analyze", analyze_medical_report)
graph.add_node("recommend", recommend_doctors)
graph.add_node("book", book_appointment)
graph.add_node("email", send_email)

# ---------------- Entry ----------------
graph.set_entry_point("analyze")

# ---------------- Routing ----------------
graph.add_conditional_edges(
    "analyze",
    lambda state: state["severity"],
    {
        "normal": END,
        "mild": "recommend",
        "critical": "recommend",
    }
)

graph.add_edge("recommend", END)
# ❗ STOP after recommend
# UI / caller decides next step

# graph.add_edge("book", "email")
# graph.add_edge("email", END)

app = graph.compile()
