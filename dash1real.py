from re import sub
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
master_df = pd.read_csv('Master_1.csv')

# master_df.index = range(100000)
# master_df['Region'] = np.random.randint(0, 214, (100000, 1))

x = []
y = [] 
for region in master_df['Region']:
    x.append(dictionary_x[region])
    y.append(dictionary_y[region])

master_df['Latitude'] = x
master_df['Longtitude'] = y

# master_df['Category'] = np.random.randint(0, 4, (100000, 1))


# for region in master_df['Region'].unique(): 
#   sub_df = master_df[master_df['Region'] == region]

  

#   sub_df['Category'] = 
#   master_df2 = master_df.concat(sub_df, axis = 0)


# print(dictionary)

master_df['Region'] = master_df['Region'].replace(dictionary)

# master_df['Category'] = master_df['Category'].replace({
#     0: 'American Cuisine', 
#     1: 'Asian Cuisine', 
#     2: 'Latin Cuisine', 
#     3: 'Drinks/Dessert'
# })

# master_df['Count'] = [1] * 100000

# one_hot = pd.get_dummies(master_df['Category'])

# master_df = master_df.drop('Category', axis = 1)
# master_df = master_df.join(one_hot)

master_df = master_df.groupby(['Region', 'Latitude', 'Longtitude'], as_index = False).sum()

master_df = master_df.astype({'Asian Cuisine': float, 'American Cuisine': float, 'Drinks/Dessert': float, 'Latin Cuisine': float})

############################################
# Repeat it twice for the second master_df2#
############################################

# make a master df
master_df2 = pd.read_csv('Master_2.csv')

# master_df.index = range(100000)
# master_df['Region'] = np.random.randint(0, 214, (100000, 1))

x = []
y = [] 
for region in master_df2['Region']:
    x.append(dictionary_x[region])
    y.append(dictionary_y[region])

master_df2['Latitude'] = x
master_df2['Longtitude'] = y

# master_df2['Category'] = np.random.randint(0, 4, (100000, 1))


# for region in master_df2['Region'].unique(): 
#   sub_df = master_df2[master_df2['Region'] == region]

  

#   sub_df['Category'] = 
#   master_df22 = master_df2.concat(sub_df, axis = 0)


# print(dictionary)

master_df2['Region'] = master_df2['Region'].replace(dictionary)

# master_df2['Category'] = master_df2['Category'].replace({
#     0: 'American Cuisine', 
#     1: 'Asian Cuisine', 
#     2: 'Latin Cuisine', 
#     3: 'Drinks/Dessert'
# })

# master_df2['Count'] = [1] * 100000

# one_hot = pd.get_dummies(master_df2['Category'])

# master_df2 = master_df2.drop('Category', axis = 1)
# master_df2 = master_df2.join(one_hot)

master_df2 = master_df2.groupby(['Region', 'Latitude', 'Longtitude'], as_index = False).sum()

master_df2 = master_df2.astype({'Department Store': float, 'Shoes': float, 'Thrift/Vintage': float})

# print(master_df)

path = open("giant.json")
geojson = json.load(path)


fig = px.choropleth_mapbox(master_df, geojson=geojson, color="Asian Cuisine", color_continuous_scale="Brwnyl",
                    locations="Region", featureidkey="properties.neighborhood", opacity = 0.7,
                    center = {"lat": 39.290675, "lon": -76.619475}, mapbox_style = 'carto-positron',
                    zoom=10.7
                   )
fig.update_geos(fitbounds="locations", visible=True, resolution=50, 
    showcoastlines=True, coastlinecolor="Black",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue")
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.update_traces({'points': [{'customdata': 'Hampden'}]})


#### IMPORT SUBTYPE CSVS ####
categories = {}
categories['Restaurants Demand'] = master_df
categories['Clothing Store Demand'] = master_df2


america = pd.read_csv("American.csv")
america['Region'] = america['Region'].replace(dictionary)

latin = pd.read_csv("Latin.csv")
latin['Region'] = latin['Region'].replace(dictionary)


drinks = pd.read_csv("Drinks.csv")
drinks['Region'] = drinks['Region'].replace(dictionary)

asian = pd.read_csv("Asian.csv")
asian['Region'] = asian['Region'].replace(dictionary)

thrift = pd.read_csv("Thrift.csv").drop(['Unnamed: 0'], axis = 1)
thrift['Region'] = thrift['Region'].replace(dictionary)

department = pd.read_csv("Department.csv").drop(['Unnamed: 0'], axis = 1)
department['Region'] = department['Region'].replace(dictionary)

shoes = pd.read_csv("Shoes.csv").drop(['Unnamed: 0'], axis = 1)
shoes['Region'] = shoes['Region'].replace(dictionary)

sub_categories = {'American Cuisine': america, "Latin Cuisine": latin, "Drinks/Dessert": drinks, "Asian Cuisine": asian, "Thrift/Vintage": thrift, "Department Store": department, "Shoes": shoes}


#############################


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
    'Drinks/Dessert' : ['Boba', 'Coffee', 'Ice Cream'],
    'Department Store' : ['Budget brands', 'Name brands'],
    'Thrift/Vintage' : ['Boutique', 'Thrift Store Chains', 'Vintage'],
    'Shoes' : ['Running Shoes', 'Sneaker', 'Outdoors', 'Shoe Warehouse']  
    }

app.layout = \
html.Div([
    html.Div(className = 'header', children='Baltimore Industry Survey Data'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(list(department_store_options.keys()), value = 'Restaurants Demand', id='store-type')
                ], className = 'store-type'),

                html.Div([
                    dcc.Dropdown(id='types-dropdown', value = 'American Cuisine')
                ], className = 'dropdown'),

                # html.Div([
                #     dcc.Dropdown(id='specific-types-dropdown', multi=True, placeholder="Select a sub-type")
                #     # dcc.Checklist(options = [
                #     #     {'label': 'PM1', 'value': 'pm1'},
                #     #     {'label': 'PM2.5', 'value': 'pm25'},
                #     #     {'label': 'PM10', 'value': 'pm10'}], value = ['pm1'], id = 'particle-type', labelStyle = {'display': 'inline-block', 'marginTop': '5px', 'padding': '10px'})
                # ])
                ], className = 'radios', style = {'padding': '0px'}),

                html.Div([
                    dcc.Graph(id='main-graph', style={'height': '73vh'}, figure = fig, hoverData={'points': [{'pointNumber': '1'}]})
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
    Output('bar-graph-1', 'figure'),
    Input('store-type', 'value'),
    Input('types-dropdown', 'value'),
    Input('main-graph', 'hoverData')
)
def graph_one(type1, type2, hoverData):
    region_name = dictionary[hoverData['points'][0]['pointNumber']]
    df = categories[type1]
    sub_df = df.groupby(['Region', 'Latitude', 'Longtitude'], as_index = False).count()
    sub_df = df[df['Region'] == region_name]

    # make a new df for a bar (just for now...)
    bar = pd.DataFrame()

    bar['Type'] = department_store_options[type1]
    list1 = []

    for options in department_store_options[type1]:
        list1.extend(sub_df[options].values)

    bar['Count'] = list1
    fig = px.bar(bar, x = 'Type', y = 'Count', color = 'Type')
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output('bar-graph-2', 'figure'),
    Input('store-type', 'value'),
    Input('types-dropdown', 'value'),
    Input('main-graph', 'hoverData')
)
def graph_two(type1, type2, hoverData):

    sub_df = sub_categories[type2]

    region_name = dictionary[hoverData['points'][0]['pointNumber']]

    sub_df = sub_df[sub_df['Region'] == region_name]
    print(sub_df)

    bar = pd.DataFrame()
    
    list_type = sub_level_options[type2]

    bar['Type'] = list_type
    list1 = sub_df.values[0][2:]
    print(list1)
    bar['Count'] = list1
    print(bar)
    fig = px.bar(bar, x = 'Type', y = 'Count', color = 'Type')
    fig.update_layout(showlegend=False)

    return fig

@app.callback(
    Output('main-graph', 'figure'),
    Input('store-type', 'value'),
    Input('types-dropdown', 'value')
)
def heatmap(type1, type2):
    colors = {'Latin Cuisine': 'Brwnyl', 'Thrift/Vintage': 'Brwnyl', 'Department Store': 'Viridis', 'Shoes': 'Cividis', 'American Cuisine': 'Viridis', 'Asian Cuisine': 'Cividis', 'Drinks/Dessert': 'Electric'}
    df = categories[type1]
    fig = px.choropleth_mapbox(df, geojson=geojson, color=f"{type2}", color_continuous_scale= colors[type2],
                    locations="Region", featureidkey="properties.neighborhood", opacity = 0.7,
                    center = {"lat": 39.290675, "lon": -76.619475}, mapbox_style = 'carto-positron',
                    zoom=10.7
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


# @app.callback(
#     Output('specific-types-dropdown', 'options'),
#     Input('types-dropdown', 'value'))
# def set_types_options(available_options):
#     return [{'label': j, 'value': j} for j in sub_level_options[available_options]]


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
    app.run_server(debug=False, port=8080)



