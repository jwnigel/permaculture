Scrapes plants data from **www.pfaf.org** and extracts about 20 characteristics for each plant

Scrape plants data from pfaf.org for all plants in (text) input file.

Collected characteristics include height, width, growth rate, leaf and flower dates, soil and pH preferences, etc.

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

prints a usage and documentation information.

### Note
***The plants.csv file here is not complete.*** You need to edit **all_plants.txt** with the plants you wish to include and run the script.
