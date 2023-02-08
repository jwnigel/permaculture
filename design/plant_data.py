import numpy as np
import pandas as pd
import random

class PlantData():

    def __init__(self):
        # Maybe make this a static element (outside the init) so that it can be edited??
        self.data = pd.read_csv('../scrapers/pfaf/all_plants.csv')

    def call_plant(df, search_name):
        # dataframe with all results
        data = df[df['CommonName'].str.lower().str.contains(search_name.lower().replace(" ", "|"))]

        # return first result for simplicity here, later allow for user to select from results
        first_result = data.iloc[0, :]

        # get attributes, so as to not return a dataframe
        common_name = first_result['CommonName']
        height = first_result['Height']
        width = first_result['Width']
        ph = first_result['pH']
        habitat = first_result['Habitat']
        return common_name, height, width # skip the others for now

class MyDesign:
    # Takes length, width and units args from design layout
    def __init__(self, length, width, units):
        self.length = length
        self.width = width
        self.units = units
        self.area = length * width
        self.overlap = 0
        # I'll use a list to store data, create dataframe when needed
        self.data = []

    def add_plant(self, common_name, x_pos, y_pos, height, width):
        self.data.append({
            'common_name': common_name, # should change to latin name as unique id
            'x, y': (x_pos, y_pos),
            'height': height,
            'width': width
        })

    def to_dataframe(self):
        df = pd.DataFrame(self.data)
        # Use groupby latin_name to sum plants
        ### *** THIS DOESNT WORK. NEED TO MAINTAIN INDIVIDUAL X- Y- POS AND COUNT TOTALS *** ###
        return df.groupby('common_name').agg({
            'common_name': 'count', 'x, y': 'unique', 'height': 'mean', 'width': 'mean'
        })
