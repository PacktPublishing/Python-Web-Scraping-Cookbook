import pandas as pd
from get_planet_data import get_planet_data

planets = get_planet_data()
planets_df = pd.DataFrame(planets).set_index('Name')
planets_df.reset_index().to_json("../../data/planets_pandas.json", orient='records')