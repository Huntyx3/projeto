import json
import requests
import numpy

SOURCE_URL = "https://raw.githubusercontent.com/Purukitto/pokemon-data.json/master/pokedex.json"
OUTPUT_FILE = "pokemon_data.json"

def map_purukitto_to_custom(p):
    # Base data
    pid = p["id"]
    name = p["name"]["english"]
    types = p["type"]
    base = p["base"]
    weight = p.get("profile", {}).get("weight", 0)
    abilities_dictlist = p.get("profile", {}).get("ability", {})
    abilities = []
    for ability in abilities_dictlist:
        abilities.append(ability[0])

    # Base form
    base_form = {
        "formName": None,
        "types": types,
        "abilities": abilities,
        "bases": {
            "HP": base["HP"],
            "Atk": base["Attack"],
            "Def": base["Defense"],
            "SpA": base["Sp. Attack"],
            "SpD": base["Sp. Defense"],
            "Spd": base["Speed"],
        },
        "weight": weight
    }

    forms = [base_form]

    # If you want to add Mega forms from elsewhere (e.g. hard‑coded or another JSON),
    # you can append them here to `forms`.

    return {
        "id": pid,
        "name": name,
        "forms": forms
    }

print("Downloading json...")
resp = requests.get(SOURCE_URL)
resp.raise_for_status()
data = resp.json()

print("Mapping to custom structure...")
result = [map_purukitto_to_custom(p) for p in data]

print(f"Writing {OUTPUT_FILE}...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Done. File saved as {OUTPUT_FILE}")

