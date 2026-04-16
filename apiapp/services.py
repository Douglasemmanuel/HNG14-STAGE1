import requests

GENDERIZE_URL = "https://api.genderize.io"
AGIFY_URL = "https://api.agify.io"
NATIONALIZE_URL = "https://api.nationalize.io"


def get_gender(name):
    res = requests.get(GENDERIZE_URL, params={"name": name})
    data = res.json()

    if not data.get("gender") or data.get("count", 0) == 0:
        raise Exception("Genderize")

    return {
        "gender": data["gender"],
        "probability": data["probability"],
        "count": data["count"]
    }


def get_age(name):
    res = requests.get(AGIFY_URL, params={"name": name})
    data = res.json()

    if data.get("age") is None:
        raise Exception("Agify")

    return {
        "age": data["age"],
        "count": data.get("count", 0)
    }


def get_nationality(name):
    res = requests.get(NATIONALIZE_URL, params={"name": name})
    data = res.json()

    countries = data.get("country", [])
    if not countries:
        raise Exception("Nationalize")

    top = max(countries, key=lambda x: x["probability"])

    return {
        "country_id": top["country_id"],
        "probability": top["probability"]
    }


def classify_age(age):
    if age <= 12:
        return "child"
    elif age <= 19:
        return "teenager"
    elif age <= 59:
        return "adult"
    return "senior"