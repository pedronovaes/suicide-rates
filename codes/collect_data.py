import numpy as np
import pandas as pd

import json
import requests
from bs4 import BeautifulSoup


def countries():
    df = pd.read_csv('../datasets/Country.csv')
    df = df[['CountryCode', 'ShortName']]
    df.columns = ['Country Code', 'Country']

    return df


if __name__ == '__main__':
    # Country names
    df_country = countries()
    print(df_country.head())
