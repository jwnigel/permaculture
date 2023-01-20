from bs4 import BeautifulSoup
import requests
import re


with open("my_apples.txt", "r") as f:
    data = f.readlines()
    for entry in data:
        data[data.index(entry)] = "-".join(entry.lower().rstrip("\n").split(" "))
    # remove duplicates with set
    data = list(set(data))
    data.sort()

print(data)
for cultivar in data[35:36]:
    print(cultivar)
    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    page = requests.get(f"https://www.orangepippin.com/varieties/apples/{cultivar}", headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    if soup.find('div', id='varietypageattributes'):
        info = soup.find('div', id='varietypageattributes').text

        print(info)

        try:
            origin_species = re.search(r"OriginsSpecies: (.*?)(Introduced|Parentage|Identification)", info).group(1)
        # If no origin species there's probably nothing else
        except AttributeError:
            origin_species = ""

        try:
            introduced = re.search(r"Introduced: (.*?)(Developed|Using)", info).group(1)
        except AttributeError:
            # checking to see if Introduced exists on it's own
            if re.search(r"Introduced: (.*?)", info):
                introduced = re.search(r"Introduced: (.{4})", info).group(1)[:4]
            else:
                introduced = ""

        try:
            picking_season = re.search(r"Picking season: (.*?)(Growing|Cropping|Picking|Keeping)", info).group(1)
        except AttributeError:
            picking_season = ""

        try:
            cropping = re.search(r"Cropping: (.*?)(Keeping|Food)", info).group(1)
        except AttributeError:
            cropping = ""

        try:
            keeping = re.search(r"Keeping \(of fruit\): (.*?)(Flavor|Food|Juice)", info).group(1)
        except AttributeError:
            keeping = ""

        try:
            primary_use = re.search(r"Food uses: (.*?)(Juice|Growing|Food)", info).group(1)
        except AttributeError:
            primary_use = ""

        # try:
        #     secondary_use = re.search(r"Food uses: (.*?)(Juice|Growing|Food)", info).group(3)
        # except AttributeError:
        #     secondary_use = ""


        print(f"origin: {origin_species}")
        print(f"introduced: {introduced}")
        print(f"picking season: {picking_season}")
        print(f"cropping: {cropping}")
        print(f"keeping: {keeping}")
        print(f"uses: {primary_use}")

    else:
        print("No info")
