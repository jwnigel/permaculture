from kivymd.uix.screen import MDScreen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.datatables.datatables import MDDataTable
from kivymd.uix.toolbar.toolbar import MDTopAppBar
from kivy.metrics import dp
import ast
import pandas as pd


data = pd.read_csv('/home/nigel/Code/permaculture/scrapers/pfaf/all_plants.csv')


def get_data_table(dataframe: pd.DataFrame, columns: list):
    column_data = columns
    row_data = dataframe[columns].to_records(index=False)
    return column_data, row_data


def filter_plants(df, filters_dict=None):
    # Define the list of valid pollinators
    growth_rate = None
    hardiness_zone = None
    pollinators = None
    flower_month = None

    if filters_dict:
        hardiness_zone = filters_dict.get('hardiness_zone')
        pollinators = filters_dict.get('pollinators')
        growth_rate = filters_dict.get('growth_rate')
        flower_month = filters_dict.get('flower_month')

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

    # if flower_month is not None:
    #     filtered_df

    return filtered_df


class DBScreen(MDScreen):
    def __init__(self, **kwargs):
        super(DBScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        top_bar = MyTopBar()
        db = MyDB()
        layout.add_widget(top_bar)
        layout.add_widget(db)
        self.add_widget(layout)

    def refresh(self, filters):
        self.clear_widgets()
        db = MyDB(filters=filters)
        self.add_widget(db)
        print('database screen refreshed')

class MyTopBar(MDTopAppBar):
    def __init__(self, **kwargs):
        super(MyTopBar, self).__init__(**kwargs)
        self.title='Search Filters'
        self.left_action_items= [
        ["home", lambda x: self.callback(x), "Home"],
        ["message-star", lambda x: self.callback(x), "Message star"],
        ["message-question", lambda x: self.callback(x), "Message question"],
        ["message-reply", lambda x: self.callback(x), "Message reply"],
        ]


class MyDB(AnchorLayout):

    def __init__(self, filters=None, **kwargs):
        super(MyDB, self).__init__(**kwargs)
        db_data = pd.read_csv('/home/nigel/Code/permaculture/scrapers/pfaf/all_plants.csv')
        db_data = filter_plants(df=db_data, filters_dict=filters)
        column_data, row_data = get_data_table(db_data, columns=['Genus','Species','CommonName','GrowthRate','Height','Width','Type', 'Pollinators', 'Flower'])
        column_widths = {'Genus': 32, 
                         'Species': 35, 
                         'CommonName': 60,
                         'GrowthRate': 22,
                         'HardinessZones': 40,
                         'Height': 16,
                         'Width': 16,
                         'Type': 30,
                         'Pollinators': 40,
                         'Leaf': 30,
                         'Flower': 30,
                         'Ripen': 30,
                         'Reproduction': 30,
                         'Soils': 60,
                         'pH': 45,
                         'Preferences': 80,
                         'Tolerances': 60,
                         'Habitat': 60,
                         'HabitatRange': 60,
                         'Edibility': 25,
                         'Medicinal': 25,
                         'OtherUses': 25}
        column_data = [(x, dp(column_widths[x])) for x in column_data]
        self.table = MDDataTable(
            column_data=column_data,
            row_data=row_data,
            use_pagination=True,
            check=True,
            rows_num=20
        )
        self.table.bind(on_row_press=self.on_row_press)
        self.table.bind(on_check_pres=self.on_row_press)
        self.add_widget(self.table)

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        print(instance_table, instance_row)
        index = instance_row.index
        cols_num = len(instance_table. column_data)
        row_num = int(index/cols_num)
        col_num = index%cols_num
        cell_row =instance_table.table_data.view_adapter.get_visible_view(row_num*cols_num)
        if cell_row.ids.check.state == 'normal':
            instance_table.table_data.select_all('normal')
            cell_row.ids.check.state = 'down'
        else:
            cell_row.ids.check.state = 'normal'
        instance_table.table_data.on_mouse_select(instance_row)



# Pollinators,Leaf,Flower,Ripen,Reproduction,Soils,pH,Preferences,Tolerances,Habitat,HabitatRange,Edibility,Medicinal,OtherUses