# Permaculture plant scraping and UI design :chestnut: :seedling: :deciduous_tree:

infos: https://github.com/jwnigel/permaculture

### Part 1 - Scraping and cleaning :ledger:
Scrapes plants data from **www.pfaf.org** and extracts about 20 characteristics for each plant

Characteristics include height, width, growth rate, leaf and flower dates, soil and pH preferences, etc.

### Usage

```
usage: main.py [-h] [options]

 Scrape plants data from pfaf.org for all plants in input file

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        TXT file of list of plants (latin names as: Genus
                        Species) you want to get data for. default is
                        "sven_plants.txt".
  -v, --verbose         print more (text) info to command line
```

#### examples:

    main.py

generates `sven_plants.csv` from scraping data for all plants in "sven_plants.txt"

    main.py -v -i design-john.txt

generates `design-john.csv` from scraping data for all plants in `design-john.txt`, while printing a `verbose` progress feedback.

     main.py -h
=======

Characteristics include height, width, growth rate, leaf and flower dates, soil and pH preferences, etc.

### Usage

```
usage: main.py [-h] [options]

 Scrape plants data from pfaf.org for all plants in input file

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        TXT file of list of plants (latin names as: Genus
                        Species) you want to get data for. default is
                        "sven_plants.txt".
  -v, --verbose         print more (text) info to command line
```

#### examples:

    main.py

generates `sven_plants.csv` from scraping data for all plants in "sven_plants.txt"

    main.py -v -i design-john.txt

generates `design-john.csv` from scraping data for all plants in `design-john.txt`, while printing a `verbose` progress feedback.

     main.py -h
=======
## I've divided this project into two parts:
### Part 1 - Scraping and cleaning :ledger: :pencil2:
#### Folder = database
I scraped data from **www.pfaf.org** and extracted about 20 characteristics for each plant

Characteristics include height, width, growth rate, leaf and flower dates, soil and pH preferences, etc.

The input is **database/all_plants.txt**, which is passed to **database/pfaf_scraper.py**, and saves a .csv file
>>>>>>> master
>>>>>>> master

prints a usage and documentation information.

### Note
***The plants.csv file here is not complete.*** You need to edit **all_plants.txt** with the plants you wish to include and run the script.

### Part 2 - UI permaculture design application :art: :paintbrush:
#### Folder = design
In progress... I want to use the plant database to create an interactive design application

I want to be able to drag and drop plants from a list to an arial photo and arrange them.

### Bonus - Apples 🍎 🍏
I've scraped apple data from **www.orangepippin.com** and extracted characteristics like year introduced, cropping and keeping ability, uses, and picking season.

The characteristic I'm most interested in is **picking season** because it allows me to organize my site and plant apples according to when they will produce. 

Could be very helpful in designing a U-pick orchard, or just for homestead design. 

Simply pass your apple varieties to **apples_scraper.py** in text file called **my_apples.txt**.
