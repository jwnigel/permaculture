import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import argparse

DEBUG = True
COLUMNS = ["Family", "Genus", "Species", "CommonName", "GrowthRate", "HardinessZones",
           "Height", "Width", "Type", "Leaf", "Flower", "Ripen", "Reproduction", "Soils",
           "pH", "Preferences", "Tolerances", "Habitat", "HabitatRange",
           "Edibility", "Medicinal", "OtherUses", "PFAF"]


# parse options
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=''' Scrape plants data from pfaf.org for all plants in input file''',
                                 usage="%(prog)s [infile]",
                                 epilog='''requirements
    This program requires Python 2.7+

examples:

  %(prog)s
     generates "all_plants.csv" from scraping data for the plants in "all_plants.txt"

  %(prog)s -v -i design-john.txt
     generates "design-john.csv" from scraping data for all plants in "design-john.txt", while printing a verbose progress feedback.

more information: https://github.com/jwnigel/permaculture
 ''')

parser.add_argument('-i', '--infile', default="all_plants.txt",
                    help='TXT file of list of plants (latin names as: Genus Species) you want to get data for. default is "all_plants.txt".')
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    help='print more (text) info to command line')
args = parser.parse_args()
VERBOSE = args.verbose

outfile = args.infile.rsplit(".",1)[0]+".csv" #TODO check if outfile is writeable (not locked by other soft) before scraping.

with open(args.infile, "r") as f:
    data = f.readlines()
    for entry in data:
        data[data.index(entry)] = re.sub("\s+"," ",entry.rstrip("\n"))
    if(DEBUG): print(data)


def get_plant_info(genus, species):

    pfaf_url = f"https://pfaf.org/user/Plant.aspx?LatinName={genus}+{species}"
    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    page = requests.get(pfaf_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the description from which we will extract the characteristics
    # Description in string and list form
    description = soup.find("meta", id="description")['content']
    description_list = description.split()

    ##### Get the characteristics #####

    # deciduous or coniferous / shrub / groundcover etc
    type = description_list[4]

    if type in ["deciduous", "coniferous"]:
        height = description_list[8]
    else:
        height = description_list[7]

    try:
        growth_rate_idx = description_list.index("rate.") - 1 # growth rate is before "rate."
        growth_rate = description_list[growth_rate_idx]
    except ValueError:
        growth_rate = "" # sometimes no growth rate

    if "by" in description_list[:15]:
        width_idx = description_list.index("by") + 1 # width is after "by"
        width = description_list[width_idx]
    else:
        width = ""

    # When the plant leafs out
    leaf = "" # Better to do this before or after if statement?
    if "leaf" in description_list:
        leaf_idx = description_list.index("leaf")
        if description_list[leaf_idx + 1] == "from":
            leaf = " ".join(description_list[leaf_idx + 2: leaf_idx + 5]).strip(",")


    # When the plant is in flower
    flower = ""
    if "flower" in description_list:
        flower_idx = description_list.index("flower")
        if description_list[flower_idx + 1] == "in":
            flower = description_list[flower_idx + 2].strip(",")
        elif description_list[flower_idx + 1] == "from":
            flower = " ".join(description_list[flower_idx + 2: flower_idx + 5]).strip(",")
        else:
            print("Error: Flower not found")

    # When the plant's seed or fruit ripens
    ripen_date = ""
    if "ripen" in description_list:
        tmp_idx = description_list.index("ripen")
        if description_list[tmp_idx + 1] == "in":
            ripen_idx = tmp_idx + 2
            ripen_date = description_list[ripen_idx].strip(".")
        elif description_list[tmp_idx + 1] == "from":
            ripen_idx = tmp_idx + 2
            ripen_date = " ".join(description_list[ripen_idx: ripen_idx + 3]).strip(".")

    # Suitable soil structure (light, medium, heavy)
    soils = ""
    soil_idx = description.find("Suitable for:")
    soil_text = description[soil_idx:description.find(".", soil_idx)]
    soils = re.findall(r"(light|medium|heavy)", soil_text)

    # Suitable pH
    ph = ""
    if "pH:" in description_list:
        ph_idx = description_list.index("pH:") + 1
        ph_list = description_list[ph_idx:]
        # check for soil or soils in the list as end of ph
        if "soils." in ph_list:
            end_idx = ph_list.index("soils.")
        elif "soils" in ph_list:
            end_idx = ph_list.index("soils")
        elif "soil." in ph_list:
            end_idx = ph_list.index("soil.")
        elif "soil" in ph_list:
            end_idx = ph_list.index("soil")
        else:
            ph = "Error: end index not found"
            end_idx=6
    ph = " ".join(ph_list[:end_idx])

    # Monoecious or dioecious ("hermaprodite")
    reproduction = re.findall(r"The species is\s(\w+)", description)[0]

    # What the plant likes
    preferences = re.findall("prefers (.*?)\ and", description)

    # What the plant can tolerate
    tolerances = re.findall("can tolerate (.*?)\.", description)

    # Get information from the table
    table = soup.find("table",{"class":"table table-hover table-striped"})

    common_name = table.find("span", id="ContentPlaceHolder1_lblCommanName").text

    family = table.find("span", id="ContentPlaceHolder1_lblFamily").text

    # String range hardiness (with -) ex: 4-8
    hardiness_range = table.find("span", id="ContentPlaceHolder1_lblUSDAhardiness").text

    # List of hardiness zones
    hardiness_zones = []
    for zone in range(int(hardiness_range[0]), int(hardiness_range[-1]) + 1):
        hardiness_zones.append(zone)

    # Ecosystems
    habitats = table.find("span", id="ContentPlaceHolder1_txtHabitats").text

    # Native range
    habitat_range = table.find("span", id="ContentPlaceHolder1_lblRange").text

    edibility = table.find("span", id="ContentPlaceHolder1_txtEdrating").text.strip()

    other_uses = table.find("span", id="ContentPlaceHolder1_txtOtherUseRating").text.strip()

    medicinal_rating = table.find("span", id="ContentPlaceHolder1_txtMedRating").text.strip()

    # print(table.prettify())

    # Add Line Space
    # print("")
    # print(f'Common name: {common_name} \nFamily: {family} \nHardiness range: {hardiness_range} \
    #     \nMedicinal rating: {medicinal_rating} \nGrowth rate: {growth_rate} \nHeight: {height} meters \nType: {type} \
    #     \nLeaf: {leaf} \nFlower: {flower} \nRipen date: {ripen_date} \nSoils: {soils} \nSoil text: {soil_text} \npH: {ph}\
    #     \nReproduction: {reproduction} \nPreferences: {preferences} \nTolerances: {tolerances}\
    #     \nHabitats: {habitats} \nHabitat range: {habitat_range} \nEdibility: {edibility} \nOther uses: {other_uses} \
        # \n \nDescription: {description}')

    return family, genus, species, common_name, growth_rate, hardiness_zones, height, width,\
            type, leaf, flower, ripen_date, reproduction, soils, ph, preferences, \
            tolerances, habitats, habitat_range, edibility, medicinal_rating, other_uses, pfaf_url


def create_df():
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(columns=COLUMNS)
    return df

df = create_df()

good = []
errors = []

if(VERBOSE): print(f"retrieving infos for")
for plant in data:
    if(VERBOSE): print(f". {plant}")
    genus= plant.split(" ")[0].strip()
    species = ' '.join(plant.split(" ")[1:])  # species gets all but first term
    try:
        df = pd.concat([df, pd.Series(get_plant_info(genus, species), index=COLUMNS)], axis=1)
        good.append(plant)
    except Exception as e:
        if(VERBOSE): print(f"** {genus} {species} : {e}")
        else : print(f"{plant}")
        errors.append(plant)
        #df = pd.concat([df, plan], axis=1)

df.T[22:].to_csv(outfile, index=False)
if(DEBUG): print(f"Non errors: {good}")
if(len(errors) > 0) : print(f"Errors: {errors}")
#TODO output errors list to errors.csv to easy correct+refetch only those.
