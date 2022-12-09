from geopy.geocoders import Nominatim
import folium
import webbrowser

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


dicoTeamCoord = create_dico_coord()
# Création de la map
coordsCenter = [41.7370229, -99.5873816]
map = folium.Map(location=coordsCenter, tiles='OpenStreetMap', zoom_start=4.3)
for team, coord in dicoTeamCoord.items():
    folium.Marker(location=coord, popup = team).add_to(map)

map.save(outfile='map.html')    

 

