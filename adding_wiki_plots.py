import unicodedata
import ast
import file_save_load as fsl

######################################################
#               adding new budgets
######################################################

fileNameDataset = 'imdb_dataset_v7_no_plots'
fileNameBudgets = '_wiki_plot_for_' + fileNameDataset
actors_amount = 6

movies = fsl.read_from_file(fileNameDataset, actors_amount)

new_plots = {}

with open('files/' + fileNameBudgets) as file:
    for entry in file:
        temp = ast.literal_eval(entry)
        title = temp[1]
        plot = temp[0]
        new_plots[title] = plot

c = 0
for title in movies:
    if title in new_plots:
        movies[title]["plot"] = unicodedata.normalize('NFKD', new_plots[title]).encode('ascii','ignore')
        c += 1

print "new plot found for:", c

print "amount of movies with plot" , len(movies)


fsl.save_to_dataset(movies,actors_amount)
