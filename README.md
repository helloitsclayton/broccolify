# Broccolify.py

A simple python script to transform a JSON file full of recipes into a `broccoli-archive` file that can be loaded into the Android recipe app [Broccoli](https://github.com/flauschtrud/broccoli).

The only content in `recipes.json` is Broccoli's demo recipe for hummus, but notably my JSON schema is hierarchical while Broccoli's is tag-based. The python script expects recipes in `recipes.json` to be arranged by top-level category (e.g., entrees, sides, desserts) and then by subcategory (e.g., cakes, cookies, tarts). Values for category keys are objects, while values for subcategory keys are arrays.

This makes it impossible to "de-broccolify" an archive exported from the Broccoli app, and I do hope to write a script which accomplishes that, so I may be adjusting the schema for `recipes.json` accordingly.
