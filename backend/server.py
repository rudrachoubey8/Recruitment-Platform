from fastapi import FastAPI
from search.embeddings import create_embedding
from search.vector_store import search, candidate_store
from ingestion.load_all_data import load_all_candidates

app = FastAPI()


@app.on_event("startup")
def startup():

    load_all_candidates()

    print("Candidates loaded:", len(candidate_store))


@app.get("/candidates")
def get_candidates():

    return {
        "total": len(candidate_store),
        "data": candidate_store
    }


@app.get("/search")
def search_candidates(query: str):

    query_vector = create_embedding(query)

    results = search(query_vector)

    return {
        "query": query,
        "results": results
    }