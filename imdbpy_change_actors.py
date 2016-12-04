import csv
import file_save_load as fsl
import unicodedata

movies = fsl.read_from_file("datasetV_20161202-044233", 3)

original_dataset = fsl.read_from_file("imdb_dataset_v6.0.2_3_actors_complete.tsv",3)

top20k = {}


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def remove_spaces(actor):
    return remove_accents(actor.lstrip().rstrip().decode('unicode-escape'))

with open("IMDB_files_link/_filtered_data/actors_scrapped_20k") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for rank, name in enumerate(reader):
        _name = name[0]
        if _name not in top20k:
            top20k[_name] = {"rank": rank + 1}

for title in movies:

    actor1 = remove_spaces(movies[title]["actor1"])
    actor2 = remove_spaces(movies[title]["actor2"])
    actor3 = remove_spaces(movies[title]["actor3"])

    # if actor1 not in top20k:
    #     print actor1, "\t", title
    # if actor2 not in top20k:
    #     print actor2, "\t", title
    # if actor3 not in top20k:
    #     print actor3, "\t", title

    new_cast = [actor1, actor2, actor3]
    old_cast = [original_dataset[title]["actor1"], original_dataset[title]["actor2"], original_dataset[title]["actor3"]]

    temp_cast = f7(new_cast + old_cast)

    updated_cast = []

    for act in temp_cast:
        if act in top20k:
            updated_cast.append(act)

    updated_cast = updated_cast[:3]

    movies[title]["actor1"] = updated_cast[0]
    movies[title]["actor1_rank"] = top20k[updated_cast[0]]["rank"]

    movies[title]["actor2"] = updated_cast[1]
    movies[title]["actor2_rank"] = top20k[updated_cast[1]]["rank"]

    movies[title]["actor3"] = updated_cast[2]
    movies[title]["actor3_rank"] = top20k[updated_cast[2]]["rank"]

# print movies["Star Wars: Episode VII - The Force Awakens (2015)"]

fsl.save_to_dataset(movies,3)
    # if title == "Star Wars: Episode VII - The Force Awakens (2015)":
    #     print title
    #     print "new", new_cast
    #     print "old", old_cast
    #     print "tmp", temp_cast
    #     print "upd", updated_cast
    #     print

