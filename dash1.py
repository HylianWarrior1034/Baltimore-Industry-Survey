import pandas as pd 
import numpy as np 
import plotly.express as px
import json
import os 
import plotly.graph_objects as go
import os 
from dash import Dash, html, dcc, Input, Output, ctx, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import numpy as np 
import functools 
import operator 


giant_list = []
center = {}
dictionary = {}
dictionary_x = {}
dictionary_y = {}
i = 0

# scan and iterate through the "json" directory
for file in os.scandir(r"json"):
    # open and load json in the files
    path = r"json/{}".format(file.name)
    f = open(path)
    data = json.load(f)

    # change "geometries" into "geometry" and make it into a list instead of a dictionary 
    temp = data['geometries'][0]
    data['geometries'] = temp
    data['geometry'] = data['geometries']
    del data['geometries']

    # add "type" and "Properties" keys to the dictionary 
    data['type'] = 'Feature'
    data['properties'] = {"neighborhood": f"{file.name[:-5]}"}

    # center of the neighborhood
    center_x = 0
    center_y = 0
    len_coord = len(data['geometry']['coordinates'][0][0])
    for lon, lat in data['geometry']['coordinates'][0][0]:
        center_x += lon
        center_y += lat

    dictionary_x[i] = round(center_x/len_coord, 6)
    dictionary_y[i] = round(center_y/len_coord, 6)

    # add the id -> neighborhood key 
    dictionary[i] = file.name[:-5]
    data['id'] = str(i)

    # add the json to the list (the list is going to get appended onto giant.json later)
    giant_list.append(data)
    # json.dump(data, write, indent = 4)

    i += 1


# this is the template we are dumping to giant.json
template = {
    "type": "FeatureCollection",
    "features": giant_list
    }

# open json and dump
with open("giant.json", "w") as write:
    json.dump(template, write)

# make a master df
master_df = pd.DataFrame()

master_df.index = range(100000)
master_df['Region'] = np.random.randint(0, 214, (100000, 1))

x = []
y = [] 
for region in master_df['Region']:
    x.append(dictionary_x[region])
    y.append(dictionary_y[region])

master_df['Latitude'] = x
master_df['Longtitude'] = y

pd_csv = pd.DataFrame()

x1 = []
y1 = []

for x, y in zip(dictionary_x.values(), dictionary_y.values()):
    x1.append(x)
    y1.append(y)
pd_csv['Latitude'] = x1
pd_csv['Longtitude'] = y1
pd_csv.to_csv('centroids.csv')

master_df2 = pd.DataFrame()

master_df['Category'] = np.random.randint(0, 4, (100000, 1))


# for region in master_df['Region'].unique(): 
#   sub_df = master_df[master_df['Region'] == region]

  

#   sub_df['Category'] = 
#   master_df2 = master_df.concat(sub_df, axis = 0)


# print(dictionary)

master_df['Region'] = master_df['Region'].replace(dictionary)

master_df['Category'] = master_df['Category'].replace({
    0: 'American Cuisine', 
    1: 'Asian Cuisine', 
    2: 'Latin Cuisine', 
    3: 'Drinks/Dessert'
})

master_df['Count'] = [1] * 100000

one_hot = pd.get_dummies(master_df['Category'])

master_df = master_df.drop('Category', axis = 1)
master_df = master_df.join(one_hot)

master_df = master_df.groupby(['Region', 'Latitude', 'Longtitude'], as_index = False).sum()

master_df = master_df.astype({'Asian Cuisine': float, 'American Cuisine': float, 'Drinks/Dessert': float, 'Latin Cuisine': float})

# print(master_df)

path = open("giant.json")
geojson = json.load(path)


fig = px.choropleth_mapbox(master_df, geojson=geojson, color="Asian Cuisine", color_continuous_scale="Brwnyl",
                    locations="Region", featureidkey="properties.neighborhood", opacity = 0.7,
                    center = {"lat": 39.290675, "lon": -76.619475}, mapbox_style = 'carto-positron',
                    zoom=10
                   )
fig.update_geos(fitbounds="locations", visible=True, resolution=50, 
    showcoastlines=True, coastlinecolor="Black",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue")
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
load_figure_template("LUX")

department_store_options = {
    'Restaurants Demand': ['American Cuisine', 'Asian Cuisine', 'Latin Cuisine', 'Drinks/Dessert'],
    'Clothing Store Demand': ['Department Store', 'Thrift/Vintage', 'Shoes']
}

sub_level_options = {
    'American Cuisine' : ['Burger', 'Steakhouse', 'Breakfast'],
    'Asian Cuisine' : ['Chinese', 'Korean', 'Japanese', 'Thai', 'Indian'],
    'Latin Cuisine' : ['Mexican', 'Tapas', 'Carribean'],
    'Drinks/Desserts' : ['Boba', 'Coffee', 'Ice Cream'],
    'Department Store' : ['Budget brands', 'Name brands'],
    'Thrift/Vintage' : ['Boutique', 'Thrift Store Chains', 'Vintage'],
    'Shoes' : ['Running Shoes', 'Sneaker', 'Outdoors', 'Shoe Warehouse']  

    }

app.layout = \
html.Div([
    html.Div(className = 'header', children='Sensor Data for 2022'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(list(department_store_options.keys()), value = 'Restaurants Demand', id='store-type')
                ], className = 'store-type'),

                html.Div([
                    dcc.Dropdown(id='types-dropdown', value = 'American Cuisine')
                ]),

                html.Div([
                    dcc.Dropdown(id='specific-types-dropdown', multi=True, placeholder="Select a sub-type")
                    # dcc.Checklist(options = [
                    #     {'label': 'PM1', 'value': 'pm1'},
                    #     {'label': 'PM2.5', 'value': 'pm25'},
                    #     {'label': 'PM10', 'value': 'pm10'}], value = ['pm1'], id = 'particle-type', labelStyle = {'display': 'inline-block', 'marginTop': '5px', 'padding': '10px'})
                ])
                ], className = 'radios', style = {'padding': '0px'}),

                html.Div([
                    dcc.Graph(id='main-graph', style={'height': '70vh'}, figure = fig)
                ], className = 'graph'),

            ], className = 'left'),

            html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph-1', style = {'height': '40vh'})
                    # html.Button("Download Data", id = "btn-download-csv", className = "downloader_btn"),
                    # dcc.Download(id="download-csv")
                ], className = 'bar-graph-1'),

                html.Div([
                    dcc.Graph(id='bar-graph-2', style = {'height': '40vh'})
                ], className = 'bar-graph-2')
            ], className = 'right')
    ], className = 'mainframe')
    
    ], className = 'main')

    # dcc.Store(id='storage'),
# ])

@app.callback(
    Output('main-graph', 'figure'),
    Input('store-type', 'value'),
    Input('types-dropdown', 'value')
)
def heatmap(type1, type2):
    colors = {'Latin Cuisine': 'Brwnyl', 'American Cuisine': 'Viridis', 'Asian Cuisine': 'Cividis', 'Drinks/Dessert': 'Electric'}
    fig = px.choropleth_mapbox(master_df, geojson=geojson, color=f"{type2}", color_continuous_scale= colors[type2],
                    locations="Region", featureidkey="properties.neighborhood", opacity = 0.7,
                    center = {"lat": 39.290675, "lon": -76.619475}, mapbox_style = 'carto-positron',
                    zoom=10
                   )

    fig.update_geos(fitbounds="locations", visible=True, resolution=50, 
        showcoastlines=True, coastlinecolor="Black",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="Blue")
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output('types-dropdown', 'options'),
    Input('store-type', 'value'))
def set_level_options(selected_industry):
    return [{'label': i, 'value': i} for i in department_store_options[selected_industry]]


@app.callback(
    Output('specific-types-dropdown', 'options'),
    Input('types-dropdown', 'value'))
def set_types_options(available_options):
    return [{'label': j, 'value': j} for j in sub_level_options[available_options]]


# @app.callback(
#     Output('specific-types-dropdown', 'value'),
#     Input('submit-button-state', 'n_clicks'),
#     State('specific-types-dropdown', 'options'))
# def set_specific_value(n_clicks, available_options):
#     return available_options[0]['value']


# @app.callback(Output('output-state', 'children'),
#               Input('submit-button-state', 'n_clicks'),
#               State('industry-radio', 'value'),
#               State('types-dropdown', 'value'),
#               State('specific-types-dropdown', 'value'))
# def update_output(n_clicks, selected_industry, selected_type, selected_sub_type):
#     return u'''
#     The Button has been pressed {} times,
#     Displaying {}: {}: {}
#     '''.format(n_clicks, selected_industry, selected_type, selected_sub_type)


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)



