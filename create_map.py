from geopy.geocoders import Nominatim
import folium
import create_dataFrame as cdf

def create_dico_coord():
    """
    Crée un dictionnaire des stades des équpes avec les coordonnées GPS associées
    
    Args:
        None
    
    Returns:
        dicoTeamCoord: dictionnaire des stades et leurs coordonnées GPS"""
        
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

def create_map():
    """
    Crée une map centré sur les Etats-Unies
    
    Return: map
    """
    coordsCenter = [41.7370229, -99.5873816]
    map = folium.Map(location=coordsCenter, tiles='OpenStreetMap', zoom_start=4.3)
    return map

def add_marker(map, dataframe, dicoTeamCoord):
    """
    Ajoute des marker au coordonbée des statdes des
    1à meilleurs scoreurs NBA à la map passé en paramètre
    
    Args: 
        map = map où la fonction ajoute les markers
        dataFrame = contient la liste des meilleurs scoreurs et leur équipe
        dicoTeamCoord = contient les coordonées des stades des équipes NBA
    
    Return:
        map avec les marker"""
    i=0
    for joueur in dataframe[0:10].itertuples():
        i+=1

        label = folium.Html("<p>" +str(i)+ ". " +joueur.Player + "<br />" +
                            joueur.Tm + "<br />" +
                            str(joueur.PPG)[0:4] + " PPG <br/></p>",
                            script=True)
        pop = folium.Popup(label, max_width=500)

        folium.CircleMarker(location=dicoTeamCoord[joueur.Tm], 
                            popup = pop,
                            radius=joueur.PPG/2, 
                            color='red',
                            fill=True,
                            fill_color='red',
                            fill_opacity=0.6).add_to(map)
    return map
#############################

#DataFrame
url = "https://www.basketball-reference.com/leagues/NBA_2023_totals.html#totals_stats::pts"
dataframe = cdf.create_dataframe(cdf.URL)
dataframe = cdf.stat_to_integer(dataframe)
dataframe = cdf.traitement_dataFrame(dataframe)
dataframe["PPG"] = dataframe["PTS"]/dataframe["G"] # Ajoute de la colonne point par game au DataFrame
dataframe = dataframe.sort_values(by="PPG", ascending=False)
dicoTeamCoord = create_dico_coord()
##############################
map = create_map()
map = add_marker(map, dataframe, dicoTeamCoord)
############################                      
    
map.save(outfile='map.html')

 
 

