import pandas as pd 
import numpy as np
import json
import os 
import random

master_df = pd.DataFrame()

master_df.index = range(100000)
master_df['Region'] = np.random.randint(0, 157, (100000, 1))

category = []
i = 0
dictionary = {}
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

    # add the id -> neighborhood key 
    dictionary[i] = file.name[:-5]
    data['id'] = str(i)

    # add the json to the list (the list is going to get appended onto giant.json later)
    # json.dump(data, write, indent = 4)

    i += 1


master_df2 = pd.DataFrame()

master_df['Category'] = np.random.randint(0, 4, (100000, 1))


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

# master_df = master_df.groupby(['Region'], as_index = False).sum()

# print(master_df.head())
asian = master_df[master_df["Asian"] == 1].drop(['American', 'Drinks/Dessert', 'Latin'], axis = 1)

print(len(asian))

