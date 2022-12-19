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
from geopy.geocoders import Nominatim
import style


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

URL = "https://www.basketball-reference.com/leagues/NBA_2023_totals.html#totals_stats::pts"