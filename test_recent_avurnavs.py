import datetime
import pandas as pd

df = pd.read_csv('avurnavs.csv', parse_dates=['date_debut_vigueur', 'date_fin_vigueur'])
latest_dates = df.groupby('region_prefecture_maritime')['date_debut_vigueur'].max()

regions = df['region_prefecture_maritime'].unique()

today = datetime.datetime.today()
target = (today - datetime.timedelta(days=3))

recent_avurnavs_regions = latest_dates[latest_dates >= target].keys()

no_avurnavs = set(regions) - set(recent_avurnavs_regions)
if len(no_avurnavs) > 0:
    raise ValueError('Regions with no recent AVURNAVs : ' + str(no_avurnavs))
