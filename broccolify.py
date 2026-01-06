import json
import os
import string
import shutil

with open('recipes.json', mode='r', encoding='utf-8') as file:
	recipes = json.load(file)

categories = []

if not os.path.exists('broccoli'): #makes dir for archive if does not already exist
	os.mkdir('broccoli')

for recipe in recipes:
	title = recipes[recipe]['title'].replace('&amp;','&')

	fileName = recipes[recipe]['title'].replace(' &amp; ',' ')
	fileName = fileName.translate(str.maketrans('', '', string.punctuation))
	fileName = fileName.replace(' ','_')

	directions = '\n'.join(map(str,recipes[recipe]['directions']))
	directions = directions.replace('&amp;','&')

	ingredients = '\n'.join(map(str,recipes[recipe]['ingredients']))
	ingredients = ingredients.replace('&amp;','&')

	if recipes[recipe]['notes']:
		notes = '\n'.join(map(str,recipes[recipe]['notes']))
		notes = notes.replace('&amp;','&')
	else:
		notes = ''

	if recipes[recipe]['src']:
		src = '\n'.join(map(str,recipes[recipe]['src']))

	for cat in recipes[recipe]['categories']:
		categories.append(cat)

	recipeDir = 'broccoli/'+fileName #makes directory for each recipe if they do not already exist
	if not os.path.exists(recipeDir):
		os.makedirs(recipeDir)

	if os.path.exists('img/'+fileName+'.jpg'): #copies over recipe image and sets imageName if it exists
		imageName = fileName+'.jpg'
		shutil.copy('img/'+fileName+'.jpg',recipeDir)
	else:
		imageName = ''

	newRecipe = {'categories':recipes[recipe]['categories'],'description':'','directions':directions,'imageName':imageName,'ingredients':ingredients,'notes':notes,'nutritionalValues':'','preparationTime':recipes[recipe]['prepTime'],'servings':recipes[recipe]['amt'],'source':src,'title':title,'favorite':False}

	recipePath = recipeDir+'/'+fileName
	with open(recipePath+'.json','w',encoding='utf-8') as file: #dumps newRecipe into fileName/fileName.json
		json.dump(newRecipe,file)

	shutil.make_archive(recipeDir,'zip',recipeDir) #zips up recipe folder
	shutil.move(recipeDir+'.zip',recipeDir+'.broccoli') #turns .zip files into .broccoli files
	shutil.rmtree(recipeDir) #removes files and dirs that have been zipped up

categories = list(set(categories)) #dedupes category list and creates categories.json
with open('broccoli/categories.json','w') as file:
	json.dump(categories,file)

shutil.make_archive('broccoli_import','zip','broccoli') #zips up archive
shutil.move('broccoli_import.zip','broccoli_import.broccoli-archive') #turns .zip into .broccoli-archive file
shutil.rmtree('broccoli') #removes files and dirs that have been zipped up