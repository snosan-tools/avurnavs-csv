import json
import os

import redis as redis_lib
import requests
import pandas as pd

REGIONS = ['atlantique', 'manche', 'méditerranée']

r = requests.get(
    'https://api.heroku.com/apps/avurnav/config-vars',
    headers={
        'Accept': 'application/vnd.heroku+json; version=3',
        'Authorization': 'Bearer ' + os.environ['HEROKU_TOKEN']
    }
)
r.raise_for_status()

redis = redis_lib.utils.from_url(r.json()['REDIS_URL'])

avurnavs = []
for region in REGIONS:
    keys = redis.keys(region + ':*')
    data = list(map(lambda e: json.loads(e), redis.mget(keys)))
    avurnavs.extend(data)

df = pd.DataFrame(avurnavs)
df.rename(
    columns={
        'content': 'contenu',
        'premar_region': 'region_prefecture_maritime',
        'title': 'titre',
        'valid_from': 'date_debut_vigueur',
        'valid_until': 'date_fin_vigueur',
        'number': 'numero_avurnav'
    },
    inplace=True
)

df = df[[
    'id', 'region_prefecture_maritime', 'numero_avurnav',
    'latitude', 'longitude', 'titre', 'contenu',
    'date_debut_vigueur', 'date_fin_vigueur'
]]

# We could have duplicates because in the new
# version of the Préfet maritime websites they
# don't expose the ID column
df.drop_duplicates(
    subset=['region_prefecture_maritime', 'numero_avurnav'],
    keep='first',
    inplace=True
)

df.to_csv('avurnavs.csv', index=False)
