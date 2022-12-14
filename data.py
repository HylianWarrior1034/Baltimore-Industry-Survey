# -*- coding: utf-8 -*-
"""Data

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cQ7rPTQ7-ZOQbcD4CdXlK365iHiB5ldS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from scipy.stats import norm
import time
import math

neighborhood_pops = pd.read_csv('/content/cleaned_neighborhood_populations.csv')
df = pd.read_csv('/centroids.csv')
df = df.rename(columns={"Latitude": "Longitude", "Longtitude": "Latitude"})

lat_min, lat_max, lon_min, lon_max = df['Latitude'].min(), df['Latitude'].max(), df['Longitude'].min(), df['Longitude'].max()

def dist(p1, p2):
  return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def generate_n_centroid(x1, y1, x2, y2, n):
    np.random.seed(int(time.time()))
    x = np.random.uniform(x1, x2, size=(n, 1))
    y = np.random.uniform(y1, y2, size=(n, 1))
    print(x[0][0])
    return [(x[i][0], y[i][0]) for i in range(n)]
C_list = generate_n_centroid(lat_min, lon_min, lat_max, lon_max, 4)
c1, c2, c3, c4 = C_list[0], C_list[1], C_list[2], C_list[3]

def exponential(d, a=9, b=-76.13):
  return a * math.exp(b * d)

def prob(A, B, C, D, h):
  ''' Find the probability biases for a region '''
  x1 = 1 + exponential(dist(A, h))
  x2 = 1 + exponential(dist(B, h))
  x3 = 1 + exponential(dist(C, h))
  x4 = 1 + exponential(dist(D, h))
  x0 = 2
  s = x1 + x2 + x3 + x4 + x0

  return [x0/s, x1/s, x2/s, x3/s, x4/s]

probArray = []
for i in range(len(df)):
  probArray.append(prob(c1, c2, c3, c4, (df.iloc[i].Latitude, df.iloc[i].Longitude)))

df['population'] = neighborhood_pops['population']
df.head()

df2 = pd.DataFrame(probArray)
df = df.join(df2)
df['survey_size'] = pd.Series([int(col * 0.15) for col in df.population])
df.head()

# elements = [1.1, 2.2, 3.3]
# probabilities = [0.2, 0.5, 0.3]
# np.random.choice(elements, 10, p=probabilities)

choices = [0, 1, 2, 3, 4]
survey_result = []
for i in range(len(df)):
  survey_result.append(np.random.choice(choices, df.survey_size[i], p=list(df.iloc[0:len(df), 4:9].iloc[i])))

import pandas as pd 

df1 = pd.DataFrame()

region_list = []
for i in range(232):
  region_list.extend([i] * len(survey_result[i]))

df1['Region'] = region_list

answer = []

for i in range(232):
  answer.extend(survey_result[i])

df1['Answer'] = answer

df1['Answer'] = df1['Answer'].replace({
    0: 'No Opinion',
    1: 'American Cuisine', 
    2: 'Asian Cuisine',
    3: 'Latin Cuisine',
    4: 'Drinks/Dessert'
})

# df1 = df1.drop(['Answer'], axis = 1)
one_hot = pd.get_dummies(df1['Answer'])

df1 = df1.drop(['Answer'], axis = 1)
df1 = df1.join(one_hot)

df1.to_csv('Master.csv')

# df1: Industry survery results for Resteraunt. Columns below