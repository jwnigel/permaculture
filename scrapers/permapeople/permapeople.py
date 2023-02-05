#!/bin/python3
# this file is part of https://github.com/jwnigel/permaculture
# copyleft : berteh (https://github.com/berteh) 
# licensed under terms of CC-BY

import requests, pandas as pd, json, re
import argparse

API_KEY_ID="Dbt02E5ZLbY4"
API_KEY_SECRET="f3b7ede2-2083-4163-b1c1-ca77e2814c5a"
DEBUG = False

CONTACT="Ben <hello@permapeople.org>"
HEADERS={'x-permapeople-key-id':API_KEY_ID,
	'x-permapeople-key-secret':API_KEY_SECRET,
	'Content-Type':'application/json',
	'charset':'utf8' }
AUTH = {'x-permapeople-key-id':API_KEY_ID,
	'x-permapeople-key-secret':API_KEY_SECRET }

DATA_COLUMNS_ORDER = ['id', 'name', 'slug', 'data', 'description', 'created_at', 'updated_at',
       'scientific_name', 'parent_id', 'version', 'type', 'link',
       'data.USDA Hardiness zone', 'data.Life cycle', 'data.Light requirement',
       'data.Water requirement', 'data.Soil type', 'data.Leaves',
       'data.Height', 'data.Layer', 'data.Utility', 'data.Edible',
       'data.Edible parts', 'data.German name', 'data.French name',
       'data.Growth', 'data.Family', 'data.Alternate name', 
       'data.Habitat', 'data.Warning', 'data.Native to', 'data.Introduced into', 
       'data.Wikipedia', 'data.Plants For A Future', 'data.Plants of the World Online Link',
       'data.1000 Seed Weight (g)']
DATA_PREFIX="data."   #set "" to loose the permapeople JSON second level information and make labels directly readable



# parse options
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=''' Scrape plants data from permapeople.org''',
                                 usage="%(prog)s [options]",
                                 epilog='''requirements
    This program requires Python 3.0+

examples:

  %(prog)s -t "full sun ground cover" -v
     generates "full sun ground cover.csv" (and .json) from the full text search results.

  %(prog)s -v -f design-john.txt
     generates "design-john.csv" from scraping data for all plants in "design-john.txt", while printing a verbose progress feedback.

more information: https://github.com/jwnigel/permaculture
 ''')

parser.add_argument('-t', '--text', default=False,
                    help='Text you want to get data for via full text search. Result is saved in a file with same name.')
parser.add_argument('-f', '--file', default=False,
                    help='Txt file with a list of plants you want to get data for via full text search.')
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    help='print more (text) info to command line')
parser.add_argument('-n', '--noCache', action='store_true', default=False,
                    help='do not save intermediate research results to their own local JSON file. Default is False.')
parser.add_argument('-d', '--debug', action='store_true', default=False,
                    help='print lots of extra obscure information to follow the script progress.')

args = parser.parse_args()
DEBUG = DEBUG or args.debug
VERBOSE = args.verbose or DEBUG





def list(last: int = 0) -> list:
	"""List plants ordered by their increasing internal (permapeople) ID. 

    Args:
		last: last ID to be excluded from list. Defaults to 0.

    Returns:
        list of the first next 100 plants, starting after the {last} id.
    """
	
	if VERBOSE: print(f"* listing 100 plants from {last} on, please be patient")
	r = requests.get("https://permapeople.org/api/plants", headers=AUTH, 
		params={'last':last})
	return ifNoHttpError(r)



def searchTxtToJson(text: str = "Malus pumila", max_results: int = -1, file_store: str = "") -> list:
	"""Performs a full-text search on the permapeople database. See https://permapeople.org/knowledgebase/api-docs.html#search-plants

    Args:
		text: text to be searched.
		max_results: maximum number of matching plants to be returned. Defaults to -1, returning all.
		file_store: save (all) search results in the given file as a list of JSON records, overwriting its content.

    Returns:
        Array of the first next 100 plants, starting after the {last} id.
    """

	if VERBOSE: print(f"* searching for {text}.")
	r = requests.post("https://permapeople.org/api/search", headers=HEADERS, 
		params={'q':text})
	plants = ifNoHttpError(r)['plants']
	if VERBOSE:
		print(f"  found {len(plants)} plants, returning {max_results}.")
	
	if (file_store != ""): # save to file, TODO make beautify from JSON optional for more performance
		json_object = json.dumps(plants, indent=2)
		with open(file_store, "w") as outfile:
			outfile.write(json_object)
		if VERBOSE: print(f"  saved search result to {file_store}.")
	
	return plants if (max_results==-1) else plants[:max_results]


"""
def update(id, content): #content must be an array of dict such as [{"key": "Edible", "value": "true" }+ ]
	if DEBUG: print(f"* updating plant {id} is not yet implemented.")
 #	data = ['data':content] 
 #	r = requests.put(f"https://permapeople.org/api/plants/{id}", headers=AUTH, 
 #		params={'q':text})
	return
"""


def searchFileToDf(file: str = "plants.txt", separator: str = "|"):
	""" 

	"""
	if VERBOSE: print(f"* gathering data for all plants in {file}.")
	t = pd.read_csv(file, sep = separator, skipinitialspace = True, header = None, 
		names=["latin"], converters={'latin':simplifySpaces}).to_numpy(dtype = str)
	frames = []
	for [p] in t	:  #TODO iterate is the worst performance on DF... got a way to vectorize the operation of search & combine ?
		outf = f"{p}.json" if(args.noCache==False) else ""
		found = searchTxtToJson(text = p, max_results = 1, file_store = outf)[0]
		df = convertPermaPeopleJsonToDf([found]) # found -> [found] since method expects an array, and json_normalize cleans the array if single element.
		frames.append(df)
	
	if DEBUG: print(f"  merging {len(frames)} records")
	details = pd.concat(frames, copy = False, ignore_index=True)

	if DEBUG: print(f"  after concat : {details.columns}")
	return details


##  Helpers ###############################################

def convertPermaPeopleJsonToDf(plants: list) -> list:
	""" Convert an array of JSON plants to a pandas DataFrame, flattening the multilevel "data" key described in 
	https://permapeople.org/knowledgebase/api-docs.html#get-a-single-plant  to multiple first-level attributes: "data.key:value"

    Args:
		plants: list of JSON plant records

    Returns:
        pandas DataFrame of the flatten records
    """	
	
	for p in plants:
		if DEBUG: print(f"  flattening 'data' for {p['name']}.")
		for d in p['data']:
			p[DATA_PREFIX+d['key']]=d['value']			
	
	df = pd.json_normalize(plants) # TODO Here I need to tell DF to use "id" as index, so that duplicates are discarded on concat. How ?
	df.drop(columns='data', inplace = True) # comment to keep original data attribute... but all its content has been copied to first level attributes anyway.
	if DEBUG: print(f"  normalized headers are {df.columns[:4]}.")
	
	return df

def loadJson(file: str ="plants.json"):
	if VERBOSE: print(f"* loading data from {file}.")
	data = pd.read_json(file)
	#if DEBUG: print(f"  loaded data of type {type(data)}.")
	return data

def ifNoHttpError(response):
	c = response.status_code
	if (200 <= c < 300): 
		return response.json()
	elif c==400: 
		print("Bad request (400)")
	elif c==404: 
		print("Not found (404)")
	elif c==503: 
		print("Service not available. Check online and/or try again later (503).\nIf it goes on get in touch with {CONTACT}.")
	else: 
		print(f"Something's wrong with the internet ({response})")
	quit()

def simplifySpaces(text: str):
	return re.sub("\s+"," ",text)



## run the app ################################################

if(args.text) :
	json = searchTxtToJson(args.text, file_store= f"{args.text}.json")
	df = convertPermaPeopleJsonToDf(json)
	df.to_csv(f"{args.text}.csv")
	if VERBOSE: print(f"single search result :\n{df}.")
	print(f"text search result is available in '{args.text}.csv'")


# todo add --load option to merge multiple permapeople.json's files from command line, eg full search history.
#t = loadJson("malus_pumila.json")
#t = convertPermaPeopleJsonToDf(j)
#print(f"result from loading from local search history file :\n{t}.")


if(args.file) :
	df = searchFileToDf(file=args.file)
	outf = args.file.rsplit(".",1)[0]
	df.to_csv(f"{outf}.csv")
	if VERBOSE: print(f"list search result :\n{df}.")
	print(f"list search result is available in '{outf}.csv'")

