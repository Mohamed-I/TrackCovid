from bs4 import BeautifulSoup as b
from collections import defaultdict
import requests
import pandas as pd
import time

# beautifulsoup4


def covid():
    ur = requests.get("https://www.worldometers.info/coronavirus/")
    beu = b(ur.content, "html.parser")

    whole_table = beu.find('table', id="main_table_countries_today")
    # table_header = whole_table.find('thead')
    # ths = table_header.find_all('th')
    table_body = whole_table.find('tbody')
    table_row = table_body.find_all('tr')

    all_column = defaultdict(list)

    countries = ['Egypt', 'Sudan', 'Chad', 'Ethiopia', 'South Sudan', 'Libya', 'Eritrea', 'CAR', 'World']

    rows = [[x] for x in table_row[7:]]     # all rows on the table
    for row_index in range(221):
        row = [x.text for x in rows[row_index][0].find_all('td')]
        if (row[0] != '' and int(row[0]) in range(10)) or row[1] in countries:
            all_column['all_countries'].append(row)

    for row in all_column['all_countries']:
        all_column['Index'].append(row[0])           # Index
        all_column['Country'].append(row[1])         # Country
        all_column['TotalCase'].append(row[2])       # TotalCases
        all_column['NewCase'].append(row[3])         # NewCases
        all_column['NewDeath'].append(row[5])        # NewDeaths
        all_column['TotalDeath'].append(row[4])      # TotalDeaths
        all_column['TotalRecovered'].append(row[6])  # TotalRecovered
        all_column['ActiveCase'].append(row[8])      # ActiveCases
        all_column['Critical'].append(row[9])        # Critical
        all_column['TotalTest'].append(row[12])      # TotalTests

    # print(all_column['NewCase'])
    covid_data = pd.DataFrame({
        'Index': all_column['Index'],
        'Country': all_column['Country'],
        'TotalCase': all_column['TotalCase'],
        'NewCase': all_column['NewCase'],
        'NewDeath': all_column['NewDeath'],
        'TotalDeath': all_column['TotalDeath'],
        'TotalRecovered': all_column['TotalRecovered'],
        'ActiveCase': all_column['ActiveCase'],
        'Critical': all_column['Critical'],
        'TotalTest': all_column['TotalTest']
    })

    covid_data.to_csv('covid.csv', index=False, encoding='utf-8')
    new_date = pd.read_csv('covid.csv')
    new_date.sort_values(by='Country', inplace=True, ascending=False)
    new_date.to_csv('sorted_date.csv', encoding='utf-8')


increment = 5
while True:

    try:
        covid()
        print(f'Data updated at [{time.ctime()}]')
    except Exception as e:
        print(e)
        print('##########>>> Connection is down <<<##########')
        if increment:
            time.sleep(increment)
            increment += 2
            continue
    increment = 5
    time.sleep(300)

