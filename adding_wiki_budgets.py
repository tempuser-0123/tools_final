import csv
import time
import ast
import file_save_load as fsl

######################################################
#               adding new budgets
######################################################

fileNameDataset = 'datasetV_20161118-080950'
fileNameBudgets = '_wiki_budg_for_' + fileNameDataset
actors_amount = 3

movies = fsl.read_from_file(fileNameDataset, actors_amount)

new_budgets = {}

dollar = True

with open('files/' + fileNameBudgets) as file:
    for entry in file:
        temp = ast.literal_eval(entry)
        title = temp[1]
        budget = temp[0]

        if "$"in budget:
            no_dollar = budget.partition("$")[2]
            dollar = True
        if "GBP" in budget:
            no_dollar = budget.partition("GBP")[2]
            dollar = False

        no_comma = no_dollar.replace(",", "")
        no_space = no_comma.replace(" ", "")

        if "million" in no_comma:
            only_number = no_space.partition("million")[0]
            budget = int(round(float(only_number) * 1000000, 0))
            if dollar:
                new_budgets[title] = budget
            else:
                new_budgets[title] = budget * 1.25
        else:
            budget = float(no_space)
            if dollar:
                new_budgets[title] = budget
            else:
                new_budgets[title] = budget * 1.25
        # new_budgets[title] = budget

c = 0
for title in movies:
    if title in new_budgets:
        movies[title]["budget"] = new_budgets[title]
        c += 1

print "new budget found for:", c

for title in movies.keys():
    if movies[title]["budget"] == "no_info":
        movies.pop(title, None)

print "amount of movies with budget" , len(movies)


fsl.save_to_dataset(movies,actors_amount)