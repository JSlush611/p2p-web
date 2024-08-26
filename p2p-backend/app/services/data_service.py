import pandas as pd

df = pd.read_csv('./data/swim_results.csv')
df['RaceDate'] = pd.to_datetime(df['RaceDate'])
df['Year'] = df['RaceDate'].dt.year
df['Time (min)'] = df['Time (ms)'] / 60000
