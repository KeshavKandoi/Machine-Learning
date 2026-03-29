

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.rag_pipeline import build_chain
from Backend.models.query_model import Query

app = FastAPI()

# ✅ Add this — fixes the OPTIONS 405 error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
def ask(query: Query):
    qa_chain = build_chain(query.video_id)
    result = qa_chain.invoke({"input": query.question})
    return {"answer": result["answer"]}