#!/bin/python3
# this file is part of https://github.com/jwnigel/permaculture
# copyleft : berteh (https://github.com/berteh) 
# licensed under terms of CC-BY

import requests, pandas as pd, json, re
import sys, argparse

API_KEY_ID="Dbt02E5ZLbY4"
API_KEY_SECRET="f3b7ede2-2083-4163-b1c1-ca77e2814c5a"
DEBUG = False
VERBOSE = False
CACHE_SEARCH_RESULTS = True

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



## command line options ######################


parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='''Scrape plants data from permapeople.org''',
                                 usage="\n  %(prog)s [actions] [options]",
                                 add_help=False,
                                 epilog='''requirements
    This program requires Python 3.0+

examples:

  %(prog)s -v --search "full sun ground cover"
     generates "full sun ground cover.csv" (and .json) from the full text search results.

  %(prog)s -v --list design-john.txt
     generates "design-john.csv" from scraping data for all plants in "design-john.txt",
     while printing a verbose progress feedback.

more information: https://github.com/jwnigel/permaculture
 ''')

actions = parser.add_argument_group('actions')
actions.add_argument('-h', '--help', action='help', help='show this help message and exit.')
actions.add_argument('-s', '--search', default=False,
                    help='search whole datase full text for matching text. Result is saved in a file with same name.')
actions.add_argument('-l', '--list', default=False,
                    help='search each line of list of plants you want to get data for, via full text search.')
actions.add_argument('-j', '--json', default=False,
                    help='load plants data in permapeople JSON format, provided as a url, file or string.')

options = parser.add_argument_group('options')
options.add_argument('-m', '--max', type = int, default=-1, help='number of results to keep from search result (per plant, when used in conjunction with --list)')	
options.add_argument('-n', '--noCache', action='store_true', default=False,
                    help='do not save intermediate research results to their own local JSON file. Default is False.')
options.add_argument('-v', '--verbose', action='store_true', default=False,
                    help='print more (text) info to command line')
options.add_argument('-d', '--debug', action='store_true', default=False,
                    help='print lots of extra obscure information to follow the script progress.')

# args = parser.parse_args() #KO in Jupyter Notebook , see https://hackmd.io/@iamfat/S1qkJ1uV8#Conflicts-with-argparse
args, unknown = parser.parse_known_args()


## public methods #################################

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
	return _ifNoHttpError(r)



def searchTxtToJson(text: str = "Malus pumila", max_results: int = args.max, file_store: str = "") -> list:
	"""Performs a full-text search on the permapeople database. See https://permapeople.org/knowledgebase/api-docs.html#search-plants

    Args:
		text: text to be searched.
		max_results: maximum number of matching plants to be returned. Defaults to -1, returning all.
		file_store: save (all) search results in the given file as a list of JSON records, overwriting its content.

    Returns:
        Array JSON records plants matching search text.
        Array is empty when no plant is found.
    """

	if VERBOSE: print(f"* searching for {text}.")
	r = requests.post("https://permapeople.org/api/search", headers=HEADERS, 
		params={'q':text})
	plants = _ifNoHttpError(r)['plants']
	if VERBOSE:
		print(f"  found {len(plants)} plants, returning {max_results}.")
	
	if (file_store != ""): # save to file, TODO make beautify from JSON optional for more performance
		json_object = json.dumps(plants, indent=2)
		with open(file_store, "w") as outfile:
			outfile.write(json_object)
		if VERBOSE: print(f"  saved search result to {file_store}.")
	
	return plants if (max_results==-1) else plants[:max_results]



def searchTxtToDf(text: str = "Malus pumila", max_results: int = args.max, file_store: str = "") -> pd.DataFrame:
	"""Performs a full-text search on the permapeople database. See https://permapeople.org/knowledgebase/api-docs.html#search-plants

    Args:
		text: text to be searched.
		max_results: maximum number of matching plants to be returned. Defaults to -1, returning all.
		file_store: save (all) search results in the given file as a list of JSON records, overwriting its content.

    Returns:
        DataFrame of plants matching search text.
    """

	json = searchTxtToJson(text, max_results, file_store)
	return _convertPermaPeopleJsonToDf(json)

		

def searchListToDf(source: str = "plants.txt", max_results: int = args.max, separator: str = "|") -> pd.DataFrame:
	""" 
	Search for each plant from a list.

	Args:
		source: list of plants to be looked for. source can be a url, str, path object or file-like object.
		max_results: maximum number of matching plants to be returned *for each plant*. Defaults to -1, returning all. 1 is common value to keep only first (and most likely) result.
		separator: Delimiter to use, per https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html#

    Returns:
        DataFrame of plants matching search text.
    """

	if VERBOSE: print(f"* gathering data for all plants in {source}.")
	t = pd.read_table(source, sep = separator, skipinitialspace = True, header = None, 
		names=["latin"], converters={'latin':_simplifySpaces}).to_numpy(dtype = str)
	res = []
	for [p] in t	:  #TODO iterate is the worst performance on DF... got a way to vectorize the operation of search & combine ?
		outf = f"{p}.json" if CACHE_SEARCH_RESULTS else ""
		founds = searchTxtToJson(text = p, max_results = max_results, file_store = outf)
		res.extend(founds)
	
	if DEBUG: print(f"  merging {len(res)} records")
	return _convertPermaPeopleJsonToDf(res)



def permaJsonTodF(source: str = "malus_pumila.json")-> pd.DataFrame:
	"""
	Load (array of) plants details in permapeople JSON format, provided as a url, str.
	and convert them to pandas DataFrame.

	Args:
		source: file (str) of array plants details, in permapeople JSON format. see https://permapeople.org/knowledgebase/api-docs.html
		
    Returns:
        DataFrame of given plants
    """

	if VERBOSE: print(f"* load permapeople plants details from {source[:40]}.")
	with open(source, 'r') as openfile:
 		json_object = json.load(openfile)
	return _convertPermaPeopleJsonToDf(json_object)


"""
def update(id, content): #content must be an array of dict such as [{"key": "Edible", "value": "true" }+ ]
	if DEBUG: print(f"* updating plant {id} is not yet implemented.")
 #	data = ['data':content] 
 #	r = requests.put(f"https://permapeople.org/api/plants/{id}", headers=AUTH, 
 #		params={'q':text})
	return
"""


## internal helpers ###############################################

def _convertPermaPeopleJsonToDf(plants: list) -> pd.DataFrame:
	""" Convert a permapeople.org list of JSON plants to a pandas DataFrame, flattening the multilevel "data" key described in 
	https://permapeople.org/knowledgebase/api-docs.html#get-a-single-plant  to multiple first-level attributes: "data.key:value"

    Args:
		plants: list of JSON plant records in permapeople

    Returns:
        pandas DataFrame of the flatten records
    """	
	
	
	
	for p in plants:
		if DEBUG: print(f"  flattening 'data' for {p['name']}.")
		for d in p['data']:
			p[DATA_PREFIX+d['key']]=d['value']			
	
	df = pd.json_normalize(plants) # TODO Here I need to tell DF to use "id" as index, so that duplicates are discarded on concat. How ?
	df.drop(columns='data', inplace = True) # comment to keep original data attribute... but all its content has been copied to first level attributes anyway.
	df.rename(columns={"id": "permapeople_id"})
	if DEBUG: print(f"  normalized headers are {df.columns[:4]}.")
	
	return df

def _ifNoHttpError(response):
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

def _simplifySpaces(text: str):
	return re.sub("\s+"," ",text)




## run from command line ##########################################


def main():
	global DEBUG, VERBOSE, CACHE_SEARCH_RESULTS
	
	if not(args.search or args.json or args.list) :
		parser.print_help()
		quit()


	print(f"running permapeople scrapper")	
	DEBUG = args.debug
	if DEBUG: print(f"  with args: {args}")
	VERBOSE = (DEBUG or args.verbose)
	CACHE_SEARCH_RESULTS = not(args.noCache)


	if(args.search):
		df = searchTxtToDf(text = args.search, max_results = args.max, file_store= f"{args.search}.json" if (args.noCache==False) else "")
		df.to_csv(f"{args.search}.csv")
		if VERBOSE: print(f"single search result :\n{df}.")
		print(f"text search result is available in '{args.search}.csv'")


	if(args.json): #TODO check if natively supports wildcards
		df = permaJsonTodF(source = args.json)
		#outf = args.json.rsplit(".",1)[0]
		#df.to_csv(f"{outf}.csv")
		#print(f"loaded data in now available in '{outf}.csv'")
		print(f"loaded json data is :\n{df}.")


	if(args.list):
		df = searchListToDf(source = args.list, max_results = args.max)
		outf = args.list.rsplit(".",1)[0]
		df.to_csv(f"{outf}.csv")
		if VERBOSE: print(f"list search result :\n{df}.")
		print(f"list search result is available in '{outf}.csv'")



if __name__ == '__main__':
    main()