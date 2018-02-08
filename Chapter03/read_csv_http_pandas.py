import pandas as pd
planets_df = pd.read_csv("http://localhost:8080/data/planets_pandas.csv", index_col='Name')
print(planets_df)