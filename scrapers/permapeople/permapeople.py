#!/bin/python3
# this file is part of https://github.com/jwnigel/permaculture
# copyleft : berteh (https://github.com/berteh) 
# licensed under terms of CC-BY

import requests, pandas as pd, json, re


API_KEY_ID="Dbt02E5ZLbY4"
API_KEY_SECRET="f3b7ede2-2083-4163-b1c1-ca77e2814c5a"
DEBUG = True

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
DATA_COLUMNS_KEEP_OTHERS = True
DATA_PREFIX="data."   #set "" to loose the permapeople JSON second level information and make labels directly readable



def list(last: int = 0) -> list:
	"""List plants ordered by their increasing internal (permapeople) ID. 

    Args:
		last: last ID to be excluded from list. Defaults to 0.

    Returns:
        list of the first next 100 plants, starting after the {last} id.
    """
	
	if DEBUG: print(f"* listing 100 plants from {last} on, please be patient")
	r = requests.get("https://permapeople.org/api/plants", headers=AUTH, 
		params={'last':last})
	return ifNoHttpError(r)



def search(text: str = "Malus pumila", max_results: int = -1, file_store: str = "") -> list:
	"""Performs a full-text search on the permapeople database. See https://permapeople.org/knowledgebase/api-docs.html#search-plants

    Args:
		text: text to be searched.
		max_results: maximum number of matching plants to be returned. Defaults to -1, returning all.
		file_store: save (all) search results in the given file as a list of JSON records, overwriting its content.

    Returns:
        Array of the first next 100 plants, starting after the {last} id.
    """

	if DEBUG: print(f"* searching for {text}.")
	r = requests.post("https://permapeople.org/api/search", headers=HEADERS, 
		params={'q':text})
	plants = ifNoHttpError(r)['plants']
	if DEBUG:
		print(f"  found {len(plants)} plants, returning {max_results}.")
	
	if (file_store != ""): # save to file, TODO make beautify from JSON optional for more performance
		json_object = json.dumps(plants, indent=2)
		with open(file_store, "w") as outfile:
			outfile.write(json_object)
		if DEBUG: print(f"  saved search result to {file_store}.")
	
	return plants if (max_results==-1) else plants[:max_results]


"""
def update(id, content): #content must be an array of dict such as [{"key": "Edible", "value": "true" }+ ]
	if DEBUG: print(f"* updating plant {id} is not yet implemented.")
 #	data = ['data':content] 
 #	r = requests.put(f"https://permapeople.org/api/plants/{id}", headers=AUTH, 
 #		params={'q':text})
	return
"""


def searchList(file: str = "plants.txt", separator: str = "|"):
	if DEBUG: print(f"* gathering data for all plants in {file}.")
	t = pd.read_csv(file, sep = separator, skipinitialspace = True, header = None, 
		names=["latin"], converters={'latin':simplifySpaces}).to_numpy(dtype = str)
	frames = []
	for [p] in t	:  #TODO iterate is the worst performance on DF... got a way to vectorize the operation of search & combine ?
		found = search(text = p, max_results = 1, file_store = f"{p}.json")[0]
		df = permaPeopleJsonToDf([found]) # found -> [found] since method expects an array, and json_normalize cleans the array if single element.
		df.drop(columns='data', inplace = True) # comment to keep original data attribute... but all its content has been copied to first level attributes anyway.
		frames.append(df)
	
	if DEBUG: print(f"  merging {len(frames)} records")
	details = pd.concat(frames, copy = False, ignore_index=True) # HERE the concat does not concat...
	return details


##  Helpers ###############################################

def permaPeopleJsonToDf(plants: list) -> list:
	"""Convert an array of JSON plants to a pandas DataFrame, flattening the multilevel "data" key described in 
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
	if DEBUG: print(f"  normalized headers are {df.columns[:4]}.")
	
	return df

def loadJson(file: str ="plants.json"):
	if DEBUG: print(f"* loading data from {file}.")
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



## run app ################################################

#j = search("Morus alba", file_store="Morus alba.json")
#t = permaPeopleJsonToDf(j)
#print(f"single search result :\n{t}.")


#t = loadJson("malus_pumila.json")
#t = permaPeopleJsonToDf(j)
#print(f"result from loading from local search history file :\n{t}.")


t = searchList(file="../pfaf/test_plants.txt")
if DEBUG: print(f"multiple plants search at once:\n{t}.")

