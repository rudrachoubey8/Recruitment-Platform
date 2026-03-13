import faiss
import numpy as np

dimension = 384
index = faiss.IndexFlatL2(dimension)

vectors = []

def add_vector(v):

    vectors.append(v)
    index.add(np.array([v]))

def search(query_vector):

    D, I = index.search(np.array([query_vector]), 5)

    return I