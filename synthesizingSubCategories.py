import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from scipy.stats import norm
import time

'''
Step 1) Import df
Step X) Create [P(Y_1), ... ,(Y_n)] for each region & each category, where P(Y_i) between 0.25 and 0.75

Step 2) For reach category, synthesize the responses for every person who selected that category. Keep region data
'''

# Constants:

# Import the master df for Resteraunts
main_df = pd.read_csv("Master_6_clothes.csv")
num_regions = 231
print(main_df.head())

# Initiliaze dataframes for the categories
category_preferences = {
    'Department' : pd.DataFrame(columns=['Region', 0, 1]),
    'Thrift' : pd.DataFrame(columns=['Region', 0, 1, 2]),
    'Shoes' : pd.DataFrame(columns=['Region', 0, 1, 2, 3]) 
}

# Find population values
populations = {
    'Department' : [],
    'Thrift' : [],
    'Shoes' : []
}
df = main_df.groupby(['Region'], as_index = False).sum()

populations['Department'].extend(df['Department'].values)
populations['Thrift'].extend(df['Thrift'].values)
populations['Shoes'].extend(df['Shoes'].values)

    
category = "Thrift"
category_df = category_preferences[category]

choice0 = []
choice1 = []
choice2 = []
# choice3 = []
# choice4 = []
# choice5 = []

for k in range(0, num_regions):
    
    number_sub_selections = category_df.shape[1] - 1
    
    probabilities = [np.random.uniform(0.1, .75) for x in range(number_sub_selections)]
    
    pop = populations[category][k]
    new_row = [np.random.binomial(pop, prob) for prob in probabilities]
    
    choice0.append(new_row[0])
    choice1.append(new_row[1])
    choice2.append(new_row[2])
    # choice3.append(new_row[3])
    # choice4.append(new_row[4])

category_df['Region'] = range(231)        
category_df[0] = choice0
category_df[1] = choice1
category_df[2] = choice2
# category_df[3] = choice3
# category_df[4] = choice4

                        
category_preferences[category].to_csv("Thrift.csv")


