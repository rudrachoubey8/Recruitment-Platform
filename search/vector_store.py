import faiss
import numpy as np

from search.embeddings import create_embedding

dimension = 384
index = faiss.IndexFlatL2(dimension)

vectors = []
candidate_store = []

def add_vector(v):

    vectors.append(v)
    index.add(np.array([v]))

def merge_json_objects(json_list):

    merged = {}

    for data in json_list:

        for key, value in data.items():

            if key not in merged:
                merged[key] = value
                continue

            # merge lists
            if isinstance(value, list):

                if not isinstance(merged[key], list):
                    merged[key] = [merged[key]]

                merged[key] = list(set(merged[key] + value))

            # merge strings
            elif isinstance(value, str):

                if value not in str(merged[key]):
                    merged[key] = str(merged[key]) + " " + value

            # keep longest numeric info
            elif isinstance(value, (int,float)):

                merged[key] = max(value, merged[key])

    return merged

def flatten_json(data):
    """
    Converts any JSON structure into plain text.
    Works for nested objects and lists.
    """

    text_parts = []

    if isinstance(data, dict):
        for key, value in data.items():
            text_parts.append(str(key))
            text_parts.append(flatten_json(value))

    elif isinstance(data, list):
        for item in data:
            text_parts.append(flatten_json(item))

    else:
        text_parts.append(str(data))

    return " ".join(text_parts)


def add_json(data):
    """
    Accepts any JSON object and adds it to vector store.
    """

    text = flatten_json(data)

    embedding = create_embedding(text)

    add_vector(embedding)

    candidate_store.append(data)


def search(query_vector):

    D, I = index.search(np.array([query_vector]), 5)

    results = []

    for idx in I[0]:
        if idx < len(candidate_store):
            results.append(candidate_store[idx])

    return results