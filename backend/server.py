from fastapi import FastAPI
from search.embeddings import create_embedding
from search.vector_store import search
app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Recruitment Platform"}

@app.get("/search")
def search_candidates(query: str):

    vector = create_embedding(query)

    results = search(vector)

    return {"results": results}