import pandas as pd

# URL of the CSV file
url = 'https://raw.githubusercontent.com/davwheat/uk-railway-stations/8418f848b8aa6c548857f656fdd93efa910a250c/stations.csv'

# Load CSV into DataFrame
df = pd.read_csv(url)

# Display first few rows
print(df.head())
