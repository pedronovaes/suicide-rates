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


def labor():
    df = pd.read_csv('../datasets/labor_data.csv')
    df.drop(['Series Code'], axis=1, inplace=True)

    total_of_unemployment = df[df['Series Name'] == 'Total of unemployment']
    total_of_unemployment_ae = df[df['Series Name'] == 'Total of unemployment with advanced education']
    total_of_unemployment_ie = df[df['Series Name'] == 'Total of unemployment with intermediate education']

    features = {
        'Country': total_of_unemployment['Country'].values,
        'Country Code': total_of_unemployment['Country Code'].values,
        'Unemployment': total_of_unemployment['2016'].values,
        'Unemployment with advanced education': total_of_unemployment_ae['2016'].values,
        'Unemployment with intermediate education': total_of_unemployment_ie['2016'].values
    }

    return pd.DataFrame.from_dict(features)


def happiness(df_country):
    df = pd.read_csv('../datasets/2016.csv')
    df = pd.merge(df, df_country, on='Country', how='left')

    df = df[
        ['Country', 'Country Code', 'Region', 'Happiness Rank',
         'Happiness Score', 'Lower Confidence Interval',
         'Upper Confidence Interval', 'Economy (GDP per Capita)', 'Family',
         'Health (Life Expectancy)', 'Freedom',
         'Trust (Government Corruption)', 'Generosity', 'Dystopia Residual']
    ]

    country = ['Taiwan', 'Slovakia', 'South Korea', 'Hong Kong', 'Kyrgyzstan',
               'Laos', 'Palestinian Territories', 'Congo (Kinshasa)',
               'Congo (Brazzaville)', 'Ivory Coast', 'Syria']

    code = ['TWN', 'SVK', 'KOR', 'HKG', 'KGZ', 'LAO',
            'PSE', 'COD', 'COG', 'CIV', 'SYR']

    for i in range(len(country)):
        df.loc[df['Country'] == country[i], 'Country Code'] = code[i]

    return df


def internet(df_country):
    r = requests.get('https://www.cia.gov/library/publications/the-world-factbook/fields/204.html#AF')
    c = r.content
    soup = BeautifulSoup(c, features='html.parser')

    data = soup.findAll('tr')[1:]

    data_dictionary = []

    for country in data:
        try:
            country_name = country.findAll('td', {'class': 'country'})[0].text.replace('\n', '')
            internet_percentage = float(country.findAll('span', {'class': 'subfield-number'})[1].text.replace('%', ''))
            data_dictionary.append({'Country': country_name, 'Percentage of internet access': internet_percentage})
        except:
            pass

    df = pd.DataFrame.from_dict(data_dictionary)
    df = pd.merge(df, df_country, on='Country', how='left')
    df = df[
        ['Country', 'Country Code', 'Percentage of internet access']
    ]

    country = [
        'Anguilla', 'Antarctica', 'Bahamas, The', 'British Virgin Islands',
        'Burma', 'Christmas Island', 'Congo, Democratic Republic of the',
        'Congo, Republic of the', 'Cook Islands', "Cote d'Ivoire", 'Curacao',
        'Czechia', 'Eswatini', 'Falkland Islands (Islas Malvinas)',
        'Faroe Islands', 'Gambia, The', 'Gaza Strip', 'Gibraltar', 'Guernsey',
        'Hong Kong', 'Jersey', 'Korea, South', 'Kyrgyzstan', 'Laos', 'Macau',
        'Micronesia, Federated States of', 'Montserrat', 'Nauru', 'Niue',
        'Norfolk Island', 'North Macedonia', 'Pitcairn Islands',
        'Saint Helena, Ascension, and Tristan da Cunha',
        'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin',
        'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines',
        'Sao Tome and Principe', 'Slovakia', 'Syria', 'Taiwan', 'Tokelau',
        'Wallis and Futuna', 'West Bank'
    ]

    code = [
        'AIA', 'ATA', 'BHS', 'VGB', 'MMR', 'CXR', 'COD', 'COG', 'COK', 'CIV',
        'CUW', 'CZE', 'SWZ', 'FLK', 'FRO', 'GMB', 'GZA', 'GIB', 'GGY', 'HKG',
        'JEY', 'KOR', 'KGZ', 'LAO', 'MAC', 'FSM', 'MSR', 'NRU', 'NIU', 'NFK',
        'MKD', 'PCN', 'SHN', 'KNA', 'LCA', 'MAF', 'SPM', 'VCT', 'STP', 'SVK',
        'SYR', 'TWN', 'TKL', 'WLF', 'PSE'
    ]

    for i in range(len(country)):
        df.loc[df['Country'] == country[i], 'Country Code'] = code[i]

    return df


def suicide(df_country):
    with open('../datasets/data.json', 'r') as file:
        obj = file.read()

    data = json.loads(obj)

    list_of_data = []

    for fact in data['fact']:
        for category in fact['dims']:
            if category == 'COUNTRY':
                country_name = fact['dims'][category]
            elif category == 'SEX':
                sex = fact['dims'][category]
        suicide_rate = fact['Value']
        list_of_data.append({
            'Country name': country_name,
            'Sex': sex,
            'Suicide rate': suicide_rate
        })

    country_names = []

    for country in list_of_data:
        country_names.append(country['Country name'])

    country_names = set(country_names)

    data_dictionary = []

    for country in country_names:
        data_dictionary.append({
            'Country': country,
            'Male Suicide Rate': '',
            'Female Suicide Rate': '',
            'Combined Suicide Rate': ''
        })

    for data in list_of_data:
        for country in data_dictionary:
            if data['Country name'] == country['Country']:
                if data['Sex'] == 'Male':
                    country['Male Suicide Rate'] = data['Suicide rate']
                elif data['Sex'] == 'Female':
                    country['Female Suicide Rate'] = data['Suicide rate']
                elif data['Sex'] == 'Both sexes':
                    country['Combined Suicide Rate'] = data['Suicide rate']

    df = pd.DataFrame.from_dict(data_dictionary)
    df.set_index(['Country'], inplace=True)
    df.sort_index(inplace=True)
    df.reset_index(inplace=True)

    df = pd.merge(df, df_country, on='Country', how='left')
    df = df[
        ['Country', 'Country Code', 'Combined Suicide Rate',
         'Male Suicide Rate', 'Female Suicide Rate']
    ]

    country = [
        'Bahamas', 'Bolivia (Plurinational State of)', 'Brunei Darussalam',
        'Czechia', "Democratic People's Republic of Korea",
        'Democratic Republic of the Congo', 'Eswatini', 'Gambia',
        'Iran (Islamic Republic of)', 'Kyrgyzstan',
        "Lao People's Democratic Republic", 'Micronesia (Federated States of)',
        'Republic of Korea', 'Republic of Moldova',
        'Republic of North Macedonia', 'Russian Federation', 'Saint Lucia',
        'Saint Vincent and the Grenadines', 'Sao Tome and Principe',
        'Slovakia', 'United Kingdom of Great Britain and Northern Ireland',
        'United Republic of Tanzania', 'United States of America',
        'Venezuela (Bolivarian Republic of)', 'Viet Nam'
    ]

    code = [
        'BHS', 'BOL', 'BRN', 'CZE', 'PRK', 'COD', 'SWZ', 'GMB', 'IRN', 'KGZ',
        'LAO', 'FSM', 'KOR', 'MDA', 'MKD', 'RUS', 'LCA', 'VCT', 'STP', 'SVK',
        'GBR', 'TZA', 'USA', 'VEN', 'VNM'
    ]

    for i in range(len(country)):
        df.loc[df['Country'] == country[i], 'Country Code'] = code[i]

    return df


def population():
    df = pd.read_csv('../datasets/API_SP.URB.TOTL.IN.ZS_DS2_en_csv_v2_248280.csv',
                     skiprows=4)
    df = df[['Country Name', 'Country Code', '2016']]
    df.columns = ['Country', 'Country Code', '2016']

    return df


def religious(df_country):
    r = requests.get('https://rationalwiki.org/wiki/Importance_of_religion_by_country')
    c = r.content
    soup = BeautifulSoup(c, features='html.parser')

    data = soup.findAll('table', {'class': 'wikitable'})
    data = data[0].findAll('td')

    religious_data = []

    for i in range(len(data)):
        if i == 0 or i % 3 == 0:
            country = data[i].text.strip()
        elif i in list(range(1, len(data), 3)):
            percentual_religious = float(data[i].text.replace('%', ''))
            religious_data.append({
                'Country': country,
                'Percentage Religious': percentual_religious
            })

    df = pd.DataFrame.from_dict(religious_data)
    df = pd.merge(df, df_country, on='Country', how='left')

    country = [
        'Hong Kong', 'The Netherlands', 'South Korea', 'Taiwan', 'Slovakia',
        'United States of America', 'Kygyzstan', 'Dominican Rebpublic',
        'Palestinian Territories', 'Laos', 'Democratic Republic of the Congo',
        'Republic of the Congo'
    ]

    code = [
        'HKG', 'NLD', 'KOR', 'TWN', 'SVK', 'USA', 'KGZ', 'DOM', 'PSE', 'LAO',
        'COD', 'COG'
    ]

    for i in range(len(country)):
        df.loc[df['Country'] == country[i], 'Country Code'] = code[i]

    df = df[['Country', 'Country Code', 'Percentage Religious']]

    return df


def health():
    df = pd.read_csv('../datasets/mental_disorder_substance_use.csv')
    df = df[df['Year'] == 2016]
    df.drop(['Year'], axis=1, inplace=True)
    df.columns = [
        'Country', 'Country Code', 'Schizophrenia', 'Bipolar disorder',
        'Eating disorders', 'Anxiety disorders', 'Drug use disorders',
        'Depression', 'Alcohol use disorders'
    ]

    return df


def save_dataframes(df_country, df_labor, df_happiness, df_health,
                    df_internet_stats, df_population_living_cities,
                    df_religious, df_suicide_rates):
    df_country.to_csv('../datasets/final/country.csv', index=False)
    df_happiness.to_csv('../datasets/final/happiness.csv', index=False)
    df_health.to_csv('../datasets/final/health.csv', index=False)
    # df_health_continents.to_csv('../datasets/final/health_continents.csv', index=False)
    df_internet_stats.to_csv('../datasets/final/internet_stats.csv', index=False)
    df_population_living_cities.to_csv('../datasets/final/population_living_cities.csv', index=False)
    df_religious.to_csv('../datasets/final/religious.csv', index=False)
    df_suicide_rates.to_csv('../datasets/final/suicide_rates.csv', index=False)
    df_labor.to_csv('../datasets/final/labor.csv', index=False)


if __name__ == '__main__':
    # Country names
    df_country = countries()
    print(df_country.head())

    # Labor
    df_labor = labor()
    print(df_labor.head())

    # Happiness
    df_happiness = happiness(df_country)
    print(df_happiness.head())

    # Internet stats
    df_internet_stats = internet(df_country)
    print(df_internet_stats.head())

    # Suicide stats
    df_suicide_rates = suicide(df_country)
    print(df_suicide_rates.head())

    # Population living in cities
    df_population_living_cities = population()
    print(df_population_living_cities.head())

    # Religious data
    df_religious = religious(df_country)
    print(df_religious.head())

    # Health data
    df_health = health()
    print(df_health.head())

    # Saving dataframes
    save_dataframes(df_country=df_country,
                    df_labor=df_labor,
                    df_happiness=df_happiness,
                    df_health=df_health,
                    df_internet_stats=df_internet_stats,
                    df_population_living_cities=df_population_living_cities,
                    df_religious=df_religious,
                    df_suicide_rates=df_suicide_rates)
