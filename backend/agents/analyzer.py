import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.state import MedicalState

from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

def safe_json_parse(text: str):
    """
    Extracts first valid JSON object from text.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("No JSON object found in LLM output")

        return json.loads(match.group())

def analyze_medical_report(state: MedicalState) -> MedicalState:
    prompt = f"""
You are a medical report analysis assistant.

Your task:
1. Summarize the medical report
2. Classify severity STRICTLY using the rules below
3. Identify disease type (if applicable)
4. Identify required medical department
5. Assume patient location as Bangalore unless stated

Severity classification rules:

NORMAL:
- No active symptoms OR
- Very mild, lifestyle-related symptoms (e.g., fatigue after long work hours)
- Normal vitals
- No functional impairment
- No medical follow-up required

MILD:
- Persistent or recurring symptoms
- Symptoms needing non-urgent consultation

CRITICAL:
- Severe or sudden symptoms
- Chest pain, breathlessness, neurological deficits
- Requires urgent care

IMPORTANT:
- Fatigue clearly caused by lifestyle factors with normal vitals MUST be NORMAL.

Return ONLY raw JSON.
Do NOT include explanations.
JSON format:
{{
  "summary": "...",
  "severity": "normal | mild | critical",
  "department": "...",
  "disease_type": "...",
  "location": "Bangalore"
}}


Medical Report:
{state["raw_input"]}

"""

    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    print("🔍 RAW LLM OUTPUT:\n", raw_output)
    try:
        result = safe_json_parse(raw_output)
    except Exception as e:
        print("⚠️ JSON parsing failed, falling back to NORMAL:", str(e))
        result = {
            "summary": raw_output if raw_output else "No significant medical issues detected.",
            "severity": "normal",
            "department": None,
            "disease_type": None,
            "location": "Bangalore"
        }

    state.update(result)
    return state
