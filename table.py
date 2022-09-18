import pandas as pd 
import numpy as np 
import plotly.express as px
import json
import os 

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
    0: 'American', 
    1: 'Asian', 
    2: 'Latin', 
    3: 'Drinks/Dessert'
})

master_df['Count'] = [1] * 100000

one_hot = pd.get_dummies(master_df['Category'])

master_df = master_df.drop('Category', axis = 1)
master_df = master_df.join(one_hot)

master_df = master_df.groupby(['Region', 'Latitude', 'Longtitude'], as_index = False).sum()

master_df = master_df.astype({'Asian': float, 'American': float, 'Drinks/Dessert': float, 'Latin': float})

region_name = "Hampden"
sub_df = master_df[master_df['Region'] == region_name]
print(sub_df)
bar = pd.DataFrame()
bar['Type'] = ['American', 'Latin', 'Asian', 'Drinks/Dessert']
list1 = []
list1.extend(sub_df['American'].values)
list1.extend(sub_df['Latin'].values)
list1.extend(sub_df['Asian'].values)
list1.extend(sub_df['Drinks/Dessert'].values)
bar['Count'] = list1
# a = sub_df['American']
# bar = pd.concat([bar, a])
fig = px.bar(bar, x = 'Type', y = 'Count', color = 'Type')
fig.show()

# path = open("giant.json")
# geojson = json.load(path)


# fig = px.choropleth_mapbox(master_df, geojson=geojson, color="Asian", color_continuous_scale="Brwnyl",
#                     locations="Region", featureidkey="properties.neighborhood", opacity = 0.7,
#                     center = {"lat": 39.290675, "lon": -76.619475}, mapbox_style = 'carto-positron',
#                     zoom=11
#                    )
# fig.update_geos(fitbounds="locations", visible=True, resolution=50, 
#     showcoastlines=True, coastlinecolor="Black",
#     showland=True, landcolor="LightGreen",
#     showocean=True, oceancolor="LightBlue",
#     showlakes=True, lakecolor="Blue")
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

# df = px.data.election()
# geojson = px.data.election_geojson()

# fig = px.choropleth(df, geojson=geojson, color="Bergeron",
#                     locations="district", featureidkey="properties.district",
#                     projection="mercator"
#                    )
# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


# f = json.load("json/abell.json")
# print(f)

# master_df = pd.DataFrame()

# master_df.index = range(100000)
# master_df['Region'] = np.random.randint(0, 50, (100000, 1))

# print(master_df.head())

# df = px.data.election()
# geojson = px.data.election_geojson()


# with open("sample.json", "w") as outfile:
#     json.dump(geojson, outfile, indent = 4)