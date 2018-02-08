import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json("geo_ips.json")
#print(df[:5])

countries_only = df.country_code
print(countries_only[:5])

#print(df.groupby('country_code').count())
counts = df.groupby('country_code').country_code.count().sort_values(ascending=False)
print(counts[:5])
counts.plot(kind='bar')
plt.show()