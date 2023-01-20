# Permaculture plant scraping and UI design :chestnut: :seedling: :deciduous_tree:

## I've divided this project into two parts:
### Part 1 - Scraping and cleaning :ledger: :pencil2:
#### Folder = database
I scraped data from **www.pfaf.org** and extracted about 20 characteristics for each plant

Characteristics include height, width, growth rate, leaf and flower dates, soil and pH preferences, etc.

The input is **database/all_plants.txt**, which is passed to **database/main.py**, and saves a .csv file

You can fork a copy and modifify the .txt file to include the plants you wish to include

***The plants.csv file here is not complete.*** You need to edit **all_plants.txt** with the plants you wish to include and run the script.

### Part 2 - UI permaculture design application :art: :paintbrush:
In progress... I want to use the plant database to create an interactive design application

I want to be able to drag and drop plants from a list to an arial photo and arrange them.

### Bonus - Apples 🍎 🍏
I've scraped apple data from **www.orangepippin.com** and extracted characteristics like year introduced, cropping and keeping ability, uses, and picking season.

The characteristic I'm most interested in is **picking season** because it allows me to organize my site and plant apples according to when they will produce. 

Could be very helpful in designing a U-pick orchard, or just for homestead design. 

Simply pass your apple varieties to **apples_scraper.py** in text file called **my_apples.txt**.
