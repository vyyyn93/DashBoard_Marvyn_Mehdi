
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

year = 2002

gapminder = px.data.gapminder() # (1)
years = gapminder["year"].unique()
data = { year:gapminder.query("year == @year") for year in years} # (2)

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country",
                        hover_data={'iso_num': 'iso_num'}) # (4)


    app.layout = html.Div(children=[

                            html.H1(id = 'Title', 
                                    children=f'Life expectancy vs GDP per capita ({year})',
                                    style={'textAlign': 'center', 'color': '#7FDBFF'}),# (5)

                            dcc.Slider(
                                id="year-slider",
                                min=1987, max=2007, step = 5,
                                value=2007,
                            ), # (7)

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Button("Play",id="Button-Play", n_clicks=0, ),
                            html.Button("Pause", id="Button-Pause", n_clicks=0,
                                         disabled=False),

                            html.Div(id='Legend', 
                            children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year {year}. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            '''),
                            
                            html.Label('Year'),

                            dcc.Interval(id='interval',
                                        interval=1*1000, # in milliseconds
                                        n_intervals=0),

    ]
    )

    @app.callback(Output(component_id='interval', component_property='disabled'),
                [Input(component_id='Button-Pause', component_property='n_clicks')])
    def stop_anim(n_clicks):
        return (n_clicks%2==0)

    @app.callback([Output(component_id='graph1', component_property='figure'), 
                   Output(component_id='Title', component_property='children'),
                   Output(component_id='Legend', component_property='children')],
                    [Input(component_id='year-slider', component_property='value')])
    def update_figure(input_value): # (3)
        return [px.scatter(data[input_value], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country"),
                f'Life expectancy vs GDP per capita ({input_value})',
                f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year {input_value}. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            ''']
    
    @app.callback(Output(component_id='year-slider', component_property='value'),
                [Input(component_id='interval', component_property='n_intervals')])
    def on_tick(n_intervals):
        if n_intervals is None: return 0
        return years[(n_intervals+1)%len(years)]
                

    app.run_server(debug=True) # (8)


#l = [Output(component_id='graph1', component_property='figure'), 
 #               Output(component_id='Title', component_property='children')]

                
    