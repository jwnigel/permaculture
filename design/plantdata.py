import numpy as np
import pandas as pd
import random

class PlantData():

    def __init__(self):
        # Maybe make this a static element (outside the init) so that it can be edited??
        self.data = pd.read_csv('../scrapers/pfaf/all_plants.csv')

    def call_plant(self, search_name):
        # dataframe with all results
        results = self.data[self.data['CommonName'].str.lower().str.contains(search_name.lower().replace(" ", "|"),na=False)]
        return results

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
