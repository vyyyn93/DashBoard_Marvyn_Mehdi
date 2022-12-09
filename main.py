import requests
from bs4 import BeautifulSoup as bs
import pandas as pd 
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from geopy.geocoders import Nominatim
import folium

def create_soup(url):
    """
    Crée une soup à partir de l'url en paramètre au format BeautifulSoup
    """
    response = requests.get(url, timeout=20)
    soup = bs(response.content, 'lxml')
    return soup

def create_dataFrame(soup):
    """
    Créer une DataFrame des statistiques des joueurs NBA.
    """
    headers = soup.find('thead') # Headers du tableau de statistique
    html_data = soup.find("tbody") # Données à parser sur les joueurs

    ## Récupère les 30 noms de chaques colonnes du tableau de statistique
    list_headers = []
    for th in headers.find_all('th'):
        list_headers.append(th.text)


    df = pd.DataFrame(columns = list_headers)

    # Récupère le texte de chaque ligne du tableau (ligne de stat) et l'ajoute dans la dataframe
    list_ligne_stat = html_data.find_all('tr', class_="full_table") 
    for tr in list_ligne_stat:
        list_data_player = tr.find_all(['th', 'td'])
        list_stat = [td.text for td in list_data_player] # Liste des stats 
        length = len(df)
        df.loc[length] = list_stat # Ajouter la liste à la DataFrame à l'index 'length'
    
    
    return df

def stat_to_integer(df):
    """
    Convertis les statistiques numérique en nombre
    """
    list_stat = df.columns.tolist()[5::] # Mets sous forme de list les statistiques à convertir (les 25 dernières)
    for i in list_stat:
        df[i] = pd.to_numeric(df[i])
    
    return df

url = "https://www.basketball-reference.com/leagues/NBA_2023_totals.html#totals_stats::pts"
soup = create_soup(url)
df = create_dataFrame(soup)
df = stat_to_integer(df)
df["PPG"] = df["PTS"]/df["G"] # Ajoute de la colonne point par game au DataFrame


if __name__ == '__main__':
    
    app = dash.Dash(__name__) 

    fig2 = px.histogram(df, 
                        x="PPG", nbins=25, 
                        labels={'PPG':'Points Per Game'},
                        opacity=0.7,
                        text_auto= True)
      
    app.layout = html.Div(children=[
                            html.H1(id = 'Title', 
                                    children=f'DashBoard NBA',
                                    style={'textAlign': 'center', 'color': '#000000'}),
                            
                            dcc.Graph(
                                id='graph1',
                                figure=fig2),
                                
                            html.Div(id='Count Player',
                                     children = 'Histogramme du nombre de point par match des ' + str(len(df)) + 
                                     ' joueur NBA',
                                     style={'textAlign': 'center', 'color': '#000000'}),
                            
                            html.Iframe(id='map', srcDoc=open("map.html", 'r').read(),
                                        width='100%', height=400)]
    )

    app.run_server(debug=True) # (8)
