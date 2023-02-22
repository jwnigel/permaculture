from kivymd.uix.screen import MDScreen
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables.datatables import MDDataTable
from kivy.metrics import dp
import ast
import pandas as pd


data = pd.read_csv('/home/nigel/code/jwnigel/permaculture/scrapers/pfaf/all_plants.csv')


def get_data_table(dataframe):
    column_data = list(dataframe.columns)
    row_data = dataframe.to_records(index=False)
    return column_data, row_data


def filter_plants(df, filters_dict=None):
    # Define the list of valid pollinators
    growth_rate = None
    hardiness_zone = None
    pollinators = None

    if filters_dict:
        hardiness_zone = filters_dict.get('hardiness_zone')
        pollinators = filters_dict.get('pollinators')
        growth_rate = filters_dict.get('growth_rate')

    filtered_df = df
    # Filter by each column if a value is provided
    # Starting with full dataframe self.data

    if growth_rate is not None:
        filtered_df = filtered_df[filtered_df['GrowthRate'].isin(growth_rate) | filtered_df['GrowthRate'].isna()]

    if hardiness_zone is not None:
        filtered_df = filtered_df[
            filtered_df['HardinessZones'].apply(lambda zones: hardiness_zone in ast.literal_eval(zones))]

    if pollinators is not None:
        print(pollinators, type(pollinators))
        # After rerunning pfaf.py scraper, I can remove the first .apply in the following line:
        print(filtered_df['Pollinators'])
        filtered_df['Pollinators'] = filtered_df['Pollinators'].apply(lambda x: str(x).split(','))
        filtered_df = filtered_df[filtered_df['Pollinators'].apply(lambda x: all(p in x for p in pollinators))]

    return filtered_df


class DBScreen(MDScreen):
    def __init__(self, **kwargs):
        super(DBScreen, self).__init__(**kwargs)
        self.add_widget(MyDB())

    def refresh(self, filters):
        self.clear_widgets()
        db = MyDB(filters=filters)
        self.add_widget(db)
        print('database screen refreshed')


class MyDB(AnchorLayout):

    def __init__(self, filters=None):
        super().__init__()
        db_data = pd.read_csv('/home/nigel/code/jwnigel/permaculture/scrapers/pfaf/all_plants.csv')
        db_data = filter_plants(df=db_data, filters_dict=filters)
        column_data, row_data = get_data_table(db_data)
        column_data = [(x, dp(60)) for x in column_data]
        table = MDDataTable(
            column_data=column_data,
            row_data=row_data,
            use_pagination=True,
            rows_num=25
        )
        self.add_widget(table)

