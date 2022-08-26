import json
import os
from pathlib import Path

import pandas as pd
import requests

AVURNAVS_FILENAME = "avurnavs.json"

response = requests.get(os.getenv("AVURNAVS_JSON_URL"))
response.raise_for_status()
with open(AVURNAVS_FILENAME, "w") as f:
    json.dump(response.json(), f)

df = pd.read_json(AVURNAVS_FILENAME)
df.rename(
    columns={
        "content": "contenu",
        "premar_region": "region_prefecture_maritime",
        "title": "titre",
        "valid_from": "date_debut_vigueur",
        "valid_until": "date_fin_vigueur",
        "number": "numero_avurnav",
    },
    inplace=True,
)

df = df[
    [
        "id",
        "region_prefecture_maritime",
        "numero_avurnav",
        "latitude",
        "longitude",
        "titre",
        "contenu",
        "date_debut_vigueur",
        "date_fin_vigueur",
    ]
]

# We could have duplicates because in the new
# version of the Préfet maritime websites they
# don't expose the ID column
df.drop_duplicates(
    subset=["region_prefecture_maritime", "numero_avurnav"], keep="first", inplace=True
)

df.to_csv("avurnavs.csv", index=False, float_format="%.10g")

Path(AVURNAVS_FILENAME).unlink()
