import requests
from bs4 import BeautifulSoup as bs
import pandas as pd 
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from geopy.geocoders import Nominatim
import json


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
df["APG"] = df["AST"]/df["G"]

if __name__ == '__main__':
    
    app = dash.Dash(__name__) 
    template = 'plotly_dark'
    histoPPG = px.histogram(df, 
                        x="PPG", nbins=25, 
                        labels={'PPG':'Points Per Game'},
                        opacity=0.7,
                        text_auto= True, template=template)

    histoAPG = px.histogram(df, 
                        x="APG", nbins=18, 
                        labels={'APG':'Assists Per Game'},
                        opacity=0.7,
                        text_auto= True,
                        template=template)
    
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }

    app.layout = html.Div(
                        [html.H1(id = 'Title', 
                                        children='DashBoard NBA',
                                        style={'textAlign': 'center', 'color': colors['text']}),
                        dcc.Tabs([
                            dcc.Tab(label='Histogamme', style={'backgroundColor':colors['background'], 'color':colors['text']},
                                children=[
                                    html.H3(style={'textAlign': 'center', 'marginTop': '40px', 'color':colors['text']},
                                            id='title histo'),
                                    dcc.Graph(
                                        id='graph1', style={'marginTop':'10px'}),

                                    dcc.RadioItems(options={'PPG':'Points Per Game', 'APG':'Assists Per Game'},
                                            value = 'PPG', inline=True, id='radioButton', style={'color':colors['text']})
                                ]
                            ),

                            dcc.Tab(label='Map', style={'backgroundColor':colors['background'], 'color':colors['text']}, 
                                    children=[
                                        html.H3('Carte des 10 meillleur scoreurs NBA', 
                                            style={'textAlign': 'center', 'color':colors['text']}),

                                        html.Iframe(id='map', 
                                            srcDoc=open("map.html", 'r', encoding='UTF8').read(),
                                            width='80%', height=400,
                                            style={'textAlign': 'center', 'marginTop': '40px', }
                                            )]
                            )]
                        )
                    ], style={'backgroundColor':colors['background'], 'background-image':colors['background']})

    @app.callback([Output(component_id='graph1', component_property='figure'),
                    Output(component_id='title histo', component_property='children')],
                  [Input(component_id= 'radioButton', component_property='value')])
    
    def update_histo(value):
        if value == 'PPG':
            return [histoPPG, 'Histogramme du nombre de point par match des ' 
                                        + str(len(df)) + ' joueur NBA']
        
        if value == 'APG':
            return [histoAPG,  'Histogramme du nombre d\'assists par match des ' 
                                        + str(len(df)) + ' joueur NBA']

    app.run_server(debug=True) # (8)
