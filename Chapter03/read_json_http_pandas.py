import pandas as pd
planets_df = pd.read_json("http://localhost:8080/data/planets_pandas.json").set_index('Name')
print(planets_df)
