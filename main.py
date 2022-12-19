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
import create_dataFrame as cdf

if __name__ == '__main__':
    #region Création de la dataFrame
    dataframe = cdf.create_dataframe(cdf.URL)
    dataframe = cdf.stat_to_integer(dataframe)
    dataframe = cdf.traitement_dataFrame(dataframe)
    #endregion

    #region Création des graphiques Plotly
    data_tab = dataframe[['Player', 'Pos', 'PPG']][0:20].transpose().values.tolist()
    data_tab.insert(0,[i for i in range(1, 21)])

    lay=go.Layout(
            paper_bgcolor=style.colors['background'],
            margin={'t':0},
            title="titre"
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
        template=style.TEMPLATE,
        title = "Histogramme du nombre de point par match des "
                + str(len(dataframe)) + " joueur NBA"
        
    )

    histoAPG = px.histogram(
        dataframe,
        x="APG", nbins=18,
        labels={'APG':'Assists Per Game'},
        opacity=0.7,
        text_auto= True,
        template=style.TEMPLATE,
        title = 'Histogramme du nombre de passe par match des '
                                        + str(len(dataframe)) + ' joueur NBA'
    )
    #endregion
    
    #region Création des composants du DashBoard
    space = html.Br()
    
    title = html.H1(
                id = 'Title',
                children='DashBoard NBA',
                style=style.H1_style
            )
    
    histo = dcc.Graph(
                id='graph1', 
                style=style.histo_style
            )

    radioItem = dcc.RadioItems(
                    options={
                        'PPG':'Points Per Game',
                        'APG':'Assists Per Game'
                    },
                    value = 'PPG',
                    inline=True,
                    labelStyle=style.radio_button_style,
                    id='radioButton'
                )
    
    titreMap = html.H3(
                    children='Carte des 10 meillleur scoreurs NBA',
                    style=style.H3_style
                )
    
    map = html.Iframe(
                id='map',
                srcDoc=open("map.html", 'r', encoding='UTF8').read(),
                width='70%', height=500,
                style=style.map_style
            )
    
    titreTable = html.H3(
                        children='Tableau des 10 meilleur scoreurs NBA',
                        style=style.H3_style
                    )

    table = dcc.Graph(
                id='graph2', 
                figure=fig, 
                style=style.tab_style
            )
    #endregion
    
    #region Création du DashBoard
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(
                    style=style.div_style,
                    children = [
                        space,
                        title,
                        dcc.Tabs(
                            children=[
                                dcc.Tab(
                                    label='Histogamme',
                                    style=style.tab_style,
                                    selected_style=style.tab_selected_style,
                                    children=[
                                        space,
                                        histo,
                                        space,
                                        html.Div(
                                            radioItem,
                                            style = style.div_style,
                                            className = "fs-5"),
                                        html.Br()
                                    ]
                                ),
                                dcc.Tab(
                                    label='Map',
                                    style=style.tab_style,
                                    selected_style=style.tab_selected_style, 
                                    children=[
                                        titreMap,
                                        html.Div(
                                            style={'text-align':'center'},
                                            children=[
                                                map,
                                                titreTable,
                                                table
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                    ]
                )
    #endregion

    #region Méthode des callback
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
    #endregion

    app.run_server(debug=True) # (8)
