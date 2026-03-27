from fastapi import FastAPI
from Backend.rag_pipeline import build_chain
from Backend.models.query_model import Query

app = FastAPI()
qa_chain = build_chain()

@app.post("/ask")
def ask(query: Query):
    # ✅ Use .invoke() instead of deprecated .run()
    result = qa_chain.invoke({"input": query.question})
    return {"answer": result["answer"]}