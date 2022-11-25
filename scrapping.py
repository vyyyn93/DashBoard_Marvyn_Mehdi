import requests
from bs4 import BeautifulSoup as bs
import pandas as pd 
import plotly.express as px

url2 = "https://www.basketball-reference.com/leagues/NBA_2023_totals.html#totals_stats::pts"
response = requests.get(url2, timeout=20)
soup = bs(response.content, 'lxml')
headers = soup.find('thead')
html_data = soup.find("tbody")
name_player = soup.find('h1')

## Récupérer les appelations de chaques colonnes du tableau de statistique
table_head = []
for th in headers.find_all('th'):
        table_head.append(th.text)
df = pd.DataFrame(columns = table_head)

# Récupère le contenu du tableau (ligne de stat) et l'ajoute dans le dataframe
for tr in html_data.find_all('tr', class_="full_table"):
        tds = tr.find_all(['th', 'td'])
        row_content = [td.text for td in tds] # Construction de la liste des données pour 1 joueur
        length = len(df)
        df.loc[length] = row_content # Ajouter la liste à la DataFrame à l'index 'length'

toNumeric = ['G', 'GS', 'MP', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'FG%', '3P%', '2P%','FT%', 'eFG%']
for i in toNumeric:
        df[i] = pd.to_numeric(df[i], errors = 'coerce')

