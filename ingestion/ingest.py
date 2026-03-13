import json

def load_hrms():

    with open("data/hrms/candidates.json") as f:
        data = json.load(f)

    return data


def load_linkedin():

    with open("data/linkedin/profiles.json") as f:
        data = json.load(f)

    return data


def load_email():

    with open("data/email/email.json") as f:
        data = json.load(f)

    return data
