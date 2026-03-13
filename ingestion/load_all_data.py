import os
import json

from search.vector_store import add_json, merge_json_objects

DATA_DIR = "data"

def load_json_files():

    all_records = []

    for root, dirs, files in os.walk(DATA_DIR):

        for file in files:

            if file.endswith(".json"):

                path = os.path.join(root, file)
                print("Loading:", path)
                with open(path, "r", encoding="utf-8") as f:

                    data = json.load(f)

                    # if file contains list of candidates
                    if isinstance(data, list):
                        all_records.extend(data)

                    # if single object
                    elif isinstance(data, dict):
                        all_records.append(data)
    return all_records

def group_candidates(records):
    """
    Group candidate records by unique identifier.
    Email is preferred.
    """
    grouped = {}

    for record in records:

        key = record.get("email") or record.get("phone") or record.get("name")

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(record)

    return grouped


def load_all_candidates():

    records = load_json_files()

    grouped_candidates = group_candidates(records)

    for key, json_list in grouped_candidates.items():

        merged_candidate = merge_json_objects(json_list)

        add_json(merged_candidate)

    print("All candidates loaded into vector store")