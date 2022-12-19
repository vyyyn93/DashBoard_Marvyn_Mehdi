from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import webbrowser

# Fonctions
def create_dataframe(url_site):
    """
    Créer une DataFrame des statistiques des joueurs NBA.

    Args:
        url: url du site à scraper

    Returns:
        dataframe=DataFrame des statistiques des joueurs NBA
    """
    response = requests.get(url_site, timeout=20)
    soup = bs(response.content, 'lxml')
    headers = soup.find('thead') # Headers du tableau de statistique
    html_data = soup.find("tbody") # Données à parser sur les joueurs

    ## Récupère les 30 noms de chaques colonnes du tableau de statistique
    list_headers = []
    for th_balise in headers.find_all('th'):
        list_headers.append(th_balise.text)

    dataframe = pd.DataFrame(columns = list_headers)

    # Récupère le texte de chaque ligne du tableau (ligne de stat) et l'ajoute dans la dataframe
    list_ligne_stat = html_data.find_all('tr', class_="full_table")
    i = 0
    for tr_balise in list_ligne_stat:
        list_data_player = tr_balise.find_all(['th', 'td'])
        list_stat = [td_balise.text for td_balise in list_data_player] # Liste des stats
        dataframe_length = len(dataframe)
        dataframe.loc[dataframe_length] = list_stat # Ajouter la liste à la DataFrame à l'index 'length'
        i+=1
    return dataframe

def stat_to_integer(dataframe):
    """
    Convertis les statistiques numérique de la dataFrame en integer.

    Args:
        dataframe: DataFrame à convertir.

    Return:
        dataframe: DataFrame convertis.
    """
    # Mets sous forme de list les statistiques à convertir (les 25 dernières)
    list_stat = dataframe.columns.tolist()[5::]
    for i in list_stat:
        dataframe[i] = pd.to_numeric(dataframe[i])
    return dataframe

def traitement_dataFrame(dataframe):
    """Effectue les traitements suivants:
        Ajout de la colonne PPG  

        Ajoute de la colonne APP

        Arrondis les valeurs à 2 chiffres significatifs

        Trie les jouers par ordre croissant de PPG
    
    Args: dataFrame des joueurs NBA
    
    Return: Data frame fonctionnelle"""
    dataframe["PPG"] = dataframe["PTS"]/dataframe["G"] # Ajoute de la colonne point par game au DataFrame
    dataframe["APG"] = dataframe["AST"]/dataframe["G"]
    dataframe = dataframe.round(2)
    dataframe = dataframe.sort_values(by="PPG", ascending=False)
    return dataframe
#############################

if __name__ == '__main__':
    #Scraping du site et création de la dataFrame
    URL = "https://www.basketball-reference.com/leagues/NBA_2023_totals.html#totals_stats::pts"
    dataframe = create_dataframe(URL)
    dataframe = stat_to_integer(dataframe)
    dataframe = traitement_dataFrame(dataframe)
    ###########################################
    # Définition des styles du DashBoard
    colors = {
        'background': '#151516',
        'text': '#0079D2'
    }
    H1_style = {
        'textAlign': 'center',
        'color': colors['text'],
        'marginTop':'20px',
        'marginBottom':'20px',
        'font-family' : 'Trebuchet MS, sans-serif'
    }
    H3_style = {
        'textAlign': 'center',
        'color': colors['text'],
        'marginTop':'30px',
        'font-family' : 'Trebuchet MS, sans-serif'
    }
    radio_button_style = {
        'color':'#FFFFFF',
        'font-family' : 'Trebuchet MS, sans-serif',
        'fontSize' : '20px',
        'padding':'30px'
    }
    tab_style={
        'backgroundColor':colors['background'],
        'color':colors['text'],
        'font-family' : 'Trebuchet MS, sans-serif',
        'text-align':'center',
        'border-radius': '4px'
        }
    tab_selected_style={
    "background": "black",
    'color': colors['text'],
    'font-family' : 'Trebuchet MS, sans-serif',
    'text-align':'center',
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    }
    map_style={
        'marginBottom':'30px'
    }
    histo_style ={
        'width':'1000px', 
        "display": "block",
        "margin-left": "auto",
        "margin-right": "auto"
    }
    TEMPLATE = 'plotly_dark'
    ####################################
    # Création des graphiques Plotly
    data_tab = dataframe[['Player', 'Pos', 'PPG']][0:20].transpose().values.tolist()
    data_tab.insert(0,[i for i in range(1, 21)])

    lay=go.Layout(paper_bgcolor=colors['background'],
        margin={'t':0}
    )

    tableau = go.Table(
                header=dict(values=['Rank','Player', 'Pos', 'PPG'],
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=data_tab,
                    fill_color='lavender',
                    align='left')
            )
   
    fig = go.Figure(data=[tableau],
                    layout=lay
            )

    histoPPG = px.histogram(
        dataframe,
        x="PPG", nbins=25,
        labels={'PPG':'Points Per Game'},
        opacity=0.7,
        text_auto= True, 
        template=TEMPLATE,
        title = "Histogramme du nombre de point par match des "
                + str(len(dataframe)) + " joueur NBA"
    )

    histoAPG = px.histogram(
        dataframe,
        x="APG", nbins=18,
        labels={'APG':'Assists Per Game'},
        opacity=0.7,
        text_auto= True,
        template=TEMPLATE,
        title = 'Histogramme du nombre de passe par match des '
                                        + str(len(dataframe)) + ' joueur NBA'
    )
    
    radioItem = dcc.RadioItems(
                    options={
                        'PPG':'Points Per Game',
                        'APG':'Assists Per Game'
                    },
                    value = 'PPG',
                    inline=True,
                    labelStyle=radio_button_style,
                    id='radioButton'
                )
    ####################################

    #Création du DashBoard
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(
                    style={'backgroundColor':colors['background']},
                    children = [
                        html.Br(),
                        html.H1(
                            id = 'Title',
                            children='DashBoard NBA',
                            style=H1_style),
                        dcc.Tabs(
                            children=[
                                dcc.Tab(
                                    label='Histogamme',
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                    children=[
                                        html.Br(),
                                        dcc.Graph(id='graph1', 
                                        style=histo_style),
                                        html.Br(),
                                        html.Div(
                                            radioItem,
                                            style =  {'text-align':'center','display': 'block'},
                                            className = "fs-5"),
                                        html.Br()
                                    ]
                                ),
                                dcc.Tab(
                                    label='Map',
                                    style=tab_style,
                                    selected_style=tab_selected_style, 
                                    children=[
                                        html.H3(
                                            children='Carte des 10 meillleur scoreurs NBA',
                                            style=H3_style
                                        ),
                                        html.Div(
                                            style={'text-align':'center'},
                                            children=[
                                                html.Iframe(
                                                    id='map',
                                                    srcDoc=open("map.html", 'r', encoding='UTF8').read(),
                                                    width='70%', height=500,
                                                    style=map_style
                                                ),
                                                html.H3(
                                                    children='Tableau des 10 meilleur scoreurs NBA',
                                                    style=H3_style
                                                ),
                                                dcc.Graph(id='graph2', figure=fig, style=tab_style)
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                    ]
                )
    ####################################

    #Méthode des callback
    @app.callback(Output(component_id='graph1', component_property='figure'),
                  [Input(component_id= 'radioButton', component_property='value')])

    def update_histo(value):
        """
        Mets à jour l'histogramme en fonction du choix sur le radioButton

        Args:
            value: Valeurs du radioButton

        Returns:
            Histogramme à afficher et son titre"""
        if value == 'PPG':
            return histoPPG

        return histoAPG
    ####################################

    app.run_server(debug=True) # (8)
