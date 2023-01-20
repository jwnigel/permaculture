from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# read in cultivars
with open("my_apples.txt", "r") as f:
    data = f.readlines()
    for entry in data:
        data[data.index(entry)] = "-".join(entry.lower().rstrip("\n").split(" "))
    # remove duplicates with set
    data = list(set(data))
    data.sort()

# initialize dataframe
df = pd.DataFrame(columns=["cultivar", "origin_species", "introduced", "picking_season", "cropping", "keeping", "primary_use"])

# iterate through cultivars, get info
for cultivar in data:
    not_found = [] # to append characteristics not found
    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    page = requests.get(f"https://www.orangepippin.com/varieties/apples/{cultivar}", headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    if soup.find('div', id='varietypageattributes'):
        info = soup.find('div', id='varietypageattributes').text

        try:
            origin_species = re.search(r"OriginsSpecies: (.*?)(Introduced|Parentage|Identification)", info).group(1)
        # If no origin species there's probably nothing else
        except AttributeError:
            origin_species = ""
            not_found.append('origin species')

        try:
            introduced = re.search(r"Introduced: (.*?)(Developed|Using)", info).group(1)
        except AttributeError:
            # checking to see if Introduced exists on it's own
            if re.search(r"Introduced: (.*?)", info):
                introduced = re.search(r"Introduced: (.{4})", info).group(1)[:4]
            else:
                introduced = ""
                not_found.append('year introduced')


        try:
            picking_season = re.search(r"Picking season: (.*?)(Growing|Cropping|Picking|Keeping)", info).group(1)
        except AttributeError:
            picking_season = ""
            not_found.append('picking season')

        try:
            cropping = re.search(r"Cropping: (.*?)(Keeping|Food)", info).group(1)
        except AttributeError:
            cropping = ""
            not_found.append('cropping')

        try:
            keeping = re.search(r"Keeping \(of fruit\): (.*?)(Flavor|Food|Juice)", info).group(1)
        except AttributeError:
            keeping = ""
            not_found.append('keeping')

        try:
            primary_use = re.search(r"Food uses: (.*?)(Juice|Growing|Food)", info).group(1)
        except AttributeError:
            primary_use = ""
            not_found.append('primary use')

        ### --- To do: add secondary use when it exists. Was having problems doing this through regex --- ###

        # try:
        #     secondary_use = re.search(r"Food uses: (.*?)(Juice|Growing|Food)", info).group(3)
        # except AttributeError:
        #     secondary_use = ""


        # Print successful / unsuccessful scrapes to terminal
        if not_found:
            print(f"Failed to find {not_found} for {cultivar}")
        else:
            print(f"Successfully scraped {cultivar}")

        # Append to dataframe
        df = pd.concat([df, pd.DataFrame({"cultivar": cultivar,
                                          "origin_species": origin_species,
                                          "introduced": introduced,
                                          "picking_season": picking_season,
                                          "cropping": cropping,
                                          "keeping": keeping,
                                          "primary_use": primary_use}, index=[0])], ignore_index=True)

    else:
        print(f"Nothing found for {cultivar}")
        # append cultivar to dataframe, will need to fill in manually
        df = pd.concat([df, pd.DataFrame({"cultivar": cultivar}, index=[0])], ignore_index=True)

# write to csv
df.to_csv("apples.csv", index=False)
