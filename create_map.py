import requests
from bs4 import BeautifulSoup as bs
import pandas as pd 
from geopy.geocoders import Nominatim
import folium
import webbrowser
import branca

#Fonctions
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

def create_dico_coord():
    dicoTeamStade = {"BRK":"Barclays Center", "BOS":"TD Garden", 
            "DAL":"American Airlines Center", "OKC":"Paycom Center", 
            "PHO": "Footprint Center", "GSW": "Chase Center",
            "CLE":"Rocket Mortgage Fieldhouse", "MIL":"Fiserv Forum", 
            "ATL":"State Farm Arena", "CHI":"United Center",
            "LAL":"Crypto.com Arena", "MIN":"Target Center",
            "POR":"Moda Center", "NYK":"Madison Square Garden",
            "HOU":"Toyota Center", "DET":"Little Caesars Arena",
            "WAS":"Capital One Arena","DEN":"Ball Arena",
            "CHO":"Charlotte", "PHI":"Wells Fargo Center", 
            "MIA":"FTX Arena", "SAC":"Golden 1 Center", 
            "ORL":"Amway Center", "MEM":"Memphis", 
            "TOR":"Toronto", "SAS":"San Antonio", 
            "NOP":"New Orlean", "IND":"Indianapolis", 
            "LAC":"Los Angeles", 'UTA':"Vivint Arena"}

    loc = Nominatim(user_agent="GetLoc")

    dicoTeamCoord = {}
    for team in dicoTeamStade.keys():
        getLocTeam = loc.geocode(dicoTeamStade[team])
        dicoTeamCoord[team]= [getLocTeam.latitude , getLocTeam.longitude]
    
    return dicoTeamCoord
#############################

#DataFrame
url = "https://www.basketball-reference.com/leagues/NBA_2023_totals.html#totals_stats::pts"
soup = create_soup(url)
df = create_dataFrame(soup)
df = stat_to_integer(df)
df["PPG"] = df["PTS"]/df["G"] # Ajoute de la colonne point par game au DataFrame
df = df.sort_values(by="PPG", ascending=False)
dicoTeamCoord = create_dico_coord()
##############################

#Création de la map
coordsCenter = [41.7370229, -99.5873816]
map = folium.Map(location=coordsCenter, tiles='OpenStreetMap', zoom_start=4.3)
###################

#Ajout des marker sur la map
i=0
for joueur in df[0:10].itertuples():
    i+=1

    label = folium.Html("<p>" +str(i)+ ". " +joueur.Player + "<br />" +
                        str(joueur.PPG)[0:4] + " PPG <br/></p>",
                        script=True)
    pop = folium.Popup(label, max_width=500)

    folium.CircleMarker(location=dicoTeamCoord[joueur.Tm], 
                        popup = pop,
                        radius=joueur.PPG/2, 
                        color='red',
                        fill=True,
                        fill_color='red',
                        fill_opacity=0.6
        ).add_to(map),
############################                      
    
map.save(outfile='map.html')
webbrowser.open('map.html') 

 
 

