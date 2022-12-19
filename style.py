#region Styles CSS utilisés por les composants du DashBoard

#Couleurs du background du dashBoard et du texte
colors = {
        'background': '#151516',
        'text': '#0079D2'
    }

# Style du titre du DashBoard
H1_style = {
    'textAlign': 'center',
    'color': colors['text'],
    'marginTop':'20px',
    'marginBottom':'20px',
    'font-family' : 'Trebuchet MS, sans-serif'
}

# Style des sous-titre du DashBoard
H3_style = {
    'textAlign': 'center',
    'color': colors['text'],
    'marginTop':'30px',
    'font-family' : 'Trebuchet MS, sans-serif'
}

# Style du composant RadioItem du DashBoard
radio_button_style = {
    'color':'#FFFFFF',
    'font-family' : 'Trebuchet MS, sans-serif',
    'fontSize' : '20px',
    'padding':'30px'
}

# Style du composant Tab lorsque le composent n'est pas actif
tab_style={
    'backgroundColor':colors['background'],
    'color':colors['text'],
    'font-family' : 'Trebuchet MS, sans-serif',
    'text-align':'center',
    'border-radius': '4px'
    }

# Style du composant Tab lorsque le composent est actif
tab_selected_style={
"background": colors['background'],
'color': colors['text'],
'border-left-color' : colors['background'],
'font-family' : 'Trebuchet MS, sans-serif',
'text-align':'center',
'align-items': 'center',
'justify-content': 'center',
'border-radius': '4px',
}

# Style du composant Iframe (map) du dashBoard
map_style={
    'marginBottom':'30px'
}

# Style des histogrammes
histo_style ={
    'width':'1000px', 
    "display": "block",
    "margin-left": "auto",
    "margin-right": "auto"
}

# Style du conteneurs 
div_style = {
    'backgroundColor':colors['background'], 
    'text-align':'center',
    'display': 'block'
}

# Template utilisé pour les graphiques plotly
TEMPLATE = 'plotly_dark'

#endregion