# pip install -U langgraph langchain-google-genai pydantic python-dotenv langsmith

import operator
from typing import TypedDict, Annotated, List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langsmith import traceable
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
import os

# ---------- Setup ----------
load_dotenv()
os.environ['LANGCHAIN_PROJECT']='UPsc essay score'

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ---------- Structured Output Schema ----------
class FullEvaluationSchema(BaseModel):
    language_feedback: str = Field(description="Feedback on language quality")
    analysis_feedback: str = Field(description="Feedback on depth of analysis")
    clarity_feedback: str = Field(description="Feedback on clarity of thought")
    overall_feedback: str = Field(description="Overall summary feedback")
    scores: List[int] = Field(description="List of 3 scores out of 10")

structured_model = model.with_structured_output(FullEvaluationSchema)

# ---------- Sample Essay ----------
essay2 = """India and AI Time

Now world change very fast because new tech call Artificial Intel… something (AI). India also want become big in this AI thing. If work hard, India can go top. But if no careful, India go back.

India have many good. We have smart student, many engine-ear, and good IT peoples. Big company like TCS, Infosys, Wipro already use AI. Government also do program “AI for All”. It want AI in farm, doctor place, school and transport.

In farm, AI help farmer know when to put seed, when rain come, how stop bug. In health, AI help doctor see sick early. In school, AI help student learn good. Government office use AI to find bad people and work fast.

But problem come also. First is many villager no have phone or internet. So AI not help them. Second, many people lose job because AI and machine do work. Poor people get more bad.

One more big problem is privacy. AI need big big data. Who take care? India still make data rule. If no strong rule, AI do bad.

India must all people together – govern, school, company and normal people. We teach AI and make sure AI not bad. Also talk to other country and learn from them.

If India use AI good way, we become strong, help poor and make better life. But if only rich use AI, and poor no get, then big bad thing happen.

So, in short, AI time in India have many hope and many danger. We must go right road. AI must help all people, not only some. Then India grow big and world say "good job India".
"""

# ---------- LangGraph State ----------
class UPSCState(TypedDict, total=False):
    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: Annotated[List[int], operator.add]
    avg_score: float

# ---------- Retry Wrapper ----------
import time

def safe_invoke(model, prompt):
    for _ in range(3):
        try:
            return model.invoke(prompt)
        except Exception as e:
            print("Rate limit hit, retrying in 40s...")
            time.sleep(40)
    raise Exception("Failed after retries")

# ---------- Single Optimized Node ----------
@traceable(name="full_evaluation", tags=["optimized"])
def full_evaluation(state: UPSCState):
    prompt = f"""
    Evaluate the following essay on:

    1. Language quality
    2. Depth of analysis
    3. Clarity of thought

    Provide:
    - Separate feedback for each
    - Score out of 10 for each (3 scores)
    - Final overall feedback

    Essay:
    {state["essay"]}
    """

    out = safe_invoke(structured_model, prompt)

    scores = out.scores if out.scores else [0, 0, 0]
    avg = sum(scores) / len(scores)

    return {
        "language_feedback": out.language_feedback,
        "analysis_feedback": out.analysis_feedback,
        "clarity_feedback": out.clarity_feedback,
        "overall_feedback": out.overall_feedback,
        "individual_scores": scores,
        "avg_score": avg
    }

# ---------- Build Graph ----------
graph = StateGraph(UPSCState)

graph.add_node("full_evaluation", full_evaluation)

graph.add_edge(START, "full_evaluation")
graph.add_edge("full_evaluation", END)

workflow = graph.compile()

# ---------- Run ----------
if __name__ == "__main__":
    result = workflow.invoke(
        {"essay": essay2},
        config={
            "run_name": "evaluate_upsc_essay",
            "tags": ["essay", "langgraph", "optimized"],
            "metadata": {
                "essay_length": len(essay2),
                "model": "gemini-2.5-flash",
                "dimensions": ["language", "analysis", "clarity"],
            },
        },
    )

    print("\n=== Evaluation Results ===\n")

    print("Language Feedback:\n", result.get("language_feedback", ""), "\n")
    print("Analysis Feedback:\n", result.get("analysis_feedback", ""), "\n")
    print("Clarity Feedback:\n", result.get("clarity_feedback", ""), "\n")
    print("Overall Feedback:\n", result.get("overall_feedback", ""), "\n")

    print("Individual Scores:", result.get("individual_scores", []))
    print("Average Score:", result.get("avg_score", 0.0))