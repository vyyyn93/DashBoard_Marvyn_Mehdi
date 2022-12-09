from geopy.geocoders import Nominatim
import folium

loc = Nominatim(user_agent="GetLoc")
getLocTeam = loc.g

coordsCenter = [41.7370229, -99.5873816]
map = folium.Map(location=coordsCenter, tiles='OpenStreetMap', zoom_start=4.3)
for team, coord in dicoTeamCoord.items():
    folium.Marker(location=coord, popup = team).add_to(map)
