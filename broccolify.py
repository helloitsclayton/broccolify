import json
import os
import string
import shutil

with open('recipes.json', mode='r', encoding='utf-8') as file:
	recipes = json.load(file)

categories = []

if not os.path.exists('broccoli'):
	os.mkdir('broccoli')

for cat in recipes:
	categories.append(cat)
	for subCat in recipes[cat]:
		categories.append(subCat)
		for index in range(len(recipes[cat][subCat])):
			currentRecipe = recipes[cat][subCat][index]
			
			directions = '\n'.join(map(str,currentRecipe['directions']))
			directions = directions.replace('&amp;','&')
			
			ingredients = '\n'.join(map(str,currentRecipe['ingredients']))
			ingredients = ingredients.replace('&amp;','&')

			notes = ''
			if currentRecipe['amt'] and currentRecipe['notes']:
				notes = '\n'.join(map(str,currentRecipe['notes']))
				notes = currentRecipe['amt']+'\n'+src
			elif currentRecipe['amt']:
				notes = currentRecipe['amt']
			elif currentRecipe['notes']:
				notes = '\n'.join(map(str,currentRecipe['notes']))
			
			src = ''
			if currentRecipe['src']:
				src = '\n'.join(map(str,currentRecipe['src']))
			
			title = currentRecipe['title'].replace('&amp;','&')

			fileName = title.replace(' &amp; ',' ')
			fileName = fileName.translate(str.maketrans('', '', string.punctuation))
			fileName = fileName.replace(' ','_')
			recipeDir = 'broccoli/'+fileName

			if not os.path.exists(recipeDir): #makes directory for each recipe if they do not already exist
				os.makedirs(recipeDir)

			imageName = ''
			if os.path.exists('img/'+fileName+'.jpg'): #copies over recipe image and sets imageName if it exists
				imageName = fileName+'.jpg'
				shutil.copy('img/'+fileName+'.jpg',recipeDir)

			newRecipe = {'categories':[cat,subCat],'description':'','directions':directions,'imageName':imageName,'ingredients':ingredients,'notes':notes,'nutritionalValues':'','preparationTime':'','servings':'','source':src,'title':title,'favorite':False}

			recipePath = recipeDir+'/'+fileName
			
			with open(recipePath+'.json','w',encoding='utf-8') as file: #dumps newRecipe into fileName.json
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