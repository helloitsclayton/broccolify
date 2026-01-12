import json
import os
import string
import shutil
import glob

shutil.unpack_archive(glob.glob('*.broccoli-archive')[0],'unpack','zip') #grabs broccoli-archive from current directory
os.remove('unpack/categories.json') #discards top-level list of categories

outputDict = {}

for recipeArc in os.listdir('unpack'): #iterates over .broccoli files in /unpack (corresponding to recipes)
	folderName = recipeArc.split('.')[0]
	recipeDir = 'unpack/'+folderName
	shutil.unpack_archive('unpack/'+recipeArc,recipeDir,'zip') #unpacks .boccoli file into its own dir
	recipeFileName = ''
	with open(recipeDir+'/'+glob.glob('*.json',root_dir=recipeDir)[0], mode='r', encoding='utf-8') as recipeJson:
		recipe = json.load(recipeJson)

	recipeFileName = recipe['title']
	recipeFileName = recipeFileName.replace(' & ',' ')
	recipeFileName = recipeFileName.translate(str.maketrans('', '', string.punctuation))
	recipeFileName = recipeFileName.replace(' ','_')

	ingredients = recipe['ingredients'].replace('&','&amp;')
	ingredients = ingredients.split('\n')
	directions = recipe['directions'].replace('&','&amp;')
	directions = directions.split('\n')
	notes = []
	if recipe['notes']:
		notes = recipe['notes'].replace('&','&amp;')
		notes = notes.split('\n')
	categories = []
	for item in recipe['categories']:
		categories.append(list(item.values())[0])

	outputDict[recipe['title']] = {'title':recipe['title'],'amt':recipe['servings'],'prepTime':recipe['preparationTime'],'desc':recipe['description'],'ingredients':ingredients,'directions':directions,'notes':notes,'src':recipe['source'].split('\n'),'categories':categories}

	if glob.glob('*.jpg',root_dir=recipeDir): #if img file exists, renames and moves to /img dir
		os.rename(recipeDir+'/'+glob.glob('*.jpg',root_dir=recipeDir)[0],recipeDir+'/'+recipeFileName+'.jpg')
		shutil.copy(recipeDir+'/'+recipeFileName+'.jpg','img')

with open('recipes.json','w') as file:
	json.dump(outputDict,file,indent='\t')

shutil.rmtree('unpack')