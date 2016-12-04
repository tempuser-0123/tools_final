import csv, helpers
import time
import imdb_parser
import file_save_load as fsl
import sys
import datetime

movies ={}
movie_temp = []
movies_amount = 0

actors_amount = 3

rejectes_movies = []
old_time = datetime.datetime.now()
with open("IMDB_files_link/_filtered_data/big_movies_4") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        year = parted[2].replace("\t","")
        # check year validity
        try:
            if year != "????" and int(year) >= 1986:
                movie_temp.append([title,{"year": year}])
        except:
            pass
        movies_amount += 1

print movies_amount, "all movies"
print len(movies), "movies amount after year filter"
######################################################
#               language filtering
######################################################

movies_with_languages = {}

with open("IMDB_files_link/_filtered_data/language.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        language = parted[2].replace("\t","")
        # this is because some movies like Avatar (2009) have more than one language
        if title not in movies_with_languages:
            movies_with_languages[title] = [language]
        else:
            movies_with_languages[title].append(language)

for title in movies_with_languages:
    languages = movies_with_languages[title]
    for language in languages:
        # if one of the languages of the movie is not english delete its entry from movies
        # there are different language descriptions in the language.list
        # like for example: English	(English Subtitles), English	(Original Version) etc
        if language == "English" \
                or language == "English	(English Subtitles)" \
                or language == "English(English subtitles)" \
                or language == "English	(Original Version)" \
                or language == "English(Original version)" \
                or language == "English(original version)" \
                or language == "English(US)" \
                or language == "English(United States)" \
                or language == "English(original text)" \
                or language == "English	(English Version)":
            break
        else:
            movies.pop(title, None)
            # rejectes_movies.append([title, "on_lang"])

print len(movies), "movies amount after language filter"

######################################################
#               ratings filtering
######################################################

with open("IMDB_files_link/_filtered_data/ratings.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # We split the string back into list but double white space delimiter,
        # since column values have different lenghts.
        # Now we easily know which index element is what
        # This is how each entry will look after split:
        # ['', '2012000000', '72', '3.7', 'Ashbah (2014)']
        # ['', '0..0.12103', '23', '7.7', 'Ashbah Beyrouth (1998)']
        rating_data = full_line.split("  ")
        title = rating_data[4]
        rating = rating_data[3]
        votes = rating_data[2]
        if title not in movies:
            pass
        else:
            movies[title].update({  "votes": votes,
                                    "rating": rating})

for title in movies.keys():
    if "rating" not in movies[title]:
        movies.pop(title, None)
        # rejectes_movies.append([title, "on_rating"])

print len(movies), "amount of movies that have rating"

######################################################
#               director filtering
######################################################

directors_raw = []
with open("IMDB_files_link/_filtered_data/directors.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        directors_raw.append(full_line)

directors_less_raw = []

temp = []
for line in directors_raw:
    if line != "":
        temp.append(line)
    else:
        # only add direcotrs that have movies listed
        if len(temp) > 1:
            directors_less_raw.append(temp)
        temp = []

movie_and_its_director = {}

for entry in directors_less_raw:
    director = entry[0]
    if "," in director:
        parted = director.partition(", ")
        # first name then surname
        director = parted[2] + " " + parted[0]
    for film in entry[1:len(entry)]:
        movie_name = film.partition("  ")[0]
        if movie_name not in movie_and_its_director:
            movie_and_its_director[movie_name] = {"director":[director]}
        else:
            movie_and_its_director[movie_name]["director"].append(director)

for title in movie_and_its_director:
    if title in movies:
        movies[title].update({"director": movie_and_its_director[title]["director"][0]})

for title in movies.keys():
    if "director" not in movies[title]:
        movies.pop(title, None)
        rejectes_movies.append([title,"on_dir"])

# print "memory then",helpers.memory()
# free up some memory
del movie_and_its_director, directors_raw, directors_less_raw, temp
# print "memory now",helpers.memory()

print len(movies), "amount of movies that have directors"

######################################################
#               genre filtering
######################################################

with open("IMDB_files_link/_filtered_data/genres.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        genre = parted[2].replace("\t","")
        if title in movies:
            movies[title].update({"genre": genre})

for title in movies.keys():
    if "genre" not in movies[title]:
        movies.pop(title, None)
        rejectes_movies.append([title,"on_genre"])

print len(movies), "amount of movies that have genre"

######################################################
#                business filtering
######################################################

business_raw = []

with open("IMDB_files_link/_filtered_data/business.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        business_raw.append(full_line)

business_less_raw = []
temp = []
for line in business_raw:
    if line != "----":
        temp.append(line)
    else:
        business_less_raw.append(temp)
        temp = []

movies_with_values = []
mandatory_count = 0
gr_count = 0
temp = []
for movie in business_less_raw:
    for entry in movie:
        if "MV" in entry:
            temp.append(entry)
            mandatory_count += 1
        if "BT" in entry:                     #uncomment to have movies with budget only
            temp.append(entry)                #comment to have movies without budget
            mandatory_count += 1              #
        if "GR" in entry:
            temp.append(entry)
            gr_count += 1
        # if "RT" in entry:
        #     temp.append(entry)
        #     mandatory_count += 1
    if mandatory_count >= 1 and gr_count > 0:   # change first condition to 2 if wanna have budget, 1 otherwise
        movies_with_values.append(temp)
    temp = []
    mandatory_count = 0
    gr_count = 0

budget_temp = []
gross_temp = []
title = ""

# print len(movies_with_values), "ALL movies that have stated at least budget and gross values"

for movie in movies_with_values:
    for entry in movie:
        if "MV" in entry:
            title = entry.partition("MV: ")[2]
        elif "BT" in entry:
            bt = entry.partition("BT: ")[2]
            budget_temp.append(bt)
        elif "GR" in entry:
            gr = entry.partition("GR: ")[2]
            gross_temp.append(gr)
    if title != "" and title in movies:
        if len(budget_temp) == 0 and movies[title]["rating"] >= 6:
            movies[title].update({"budget": "no_info", "gross": gross_temp})
        else:
            movies[title].update({"budget": budget_temp, "gross": gross_temp})
    title = ""
    budget_temp = []
    gross_temp = []

for title in movies.keys():
    if "gross" not in movies[title]:
        movies.pop(title, None)

small_wide_temp = []
big_wide_temp = []
usa_temp = []
other_temp = []

for title in movies:
    all_gross = movies[title]["gross"]
    for gross in all_gross:
        try:
            if "(worldwide)" in gross:
                gross_temp = gross.partition(" (worldwide)")[0]
                if "GBP" in gross_temp:
                    gross_temp = gross_temp.partition("GBP ")[2]
                    gross_temp = gross_temp.replace(",", "")
                    small_wide_temp.append(int(round(int(gross_temp)*1.25, 0)))
                elif "USD" in gross_temp:
                    gross_temp = gross_temp.partition("USD ")[2]
                    gross_temp = gross_temp.replace(",","")
                    small_wide_temp.append(int(gross_temp))
                else:
                    gross_temp = gross_temp.partition(" ")[2]
                    gross_temp = gross_temp.replace(",","")
                    small_wide_temp.append(int(gross_temp))
            elif "(Worldwide)" in gross:
                gross_temp = gross.partition(" (Worldwide)")[0]
                if "GBP" in gross_temp:
                    gross_temp = gross_temp.partition("GBP ")[2]
                    gross_temp = gross_temp.replace(",", "")
                    big_wide_temp.append(int(round(int(gross_temp)*1.25, 0)))
                elif "USD" in gross_temp:
                    gross_temp = gross_temp.partition("USD ")[2]
                    gross_temp = gross_temp.replace(",","")
                    big_wide_temp.append(int(gross_temp))
                else:
                    gross_temp = gross_temp.partition(" ")[2]
                    gross_temp = gross_temp.replace(",","")
                    big_wide_temp.append(int(gross_temp))
            elif "(USA)" in gross:
                gross_temp = gross.partition(" (USA)")[0]
                if "GBP" in gross_temp:
                    gross_temp = gross_temp.partition("GBP ")[2]
                    gross_temp = gross_temp.replace(",", "")
                    usa_temp.append(int(round(int(gross_temp)*1.25, 0)))
                elif "USD" in gross_temp:
                    gross_temp = gross_temp.partition("USD ")[2]
                    gross_temp = gross_temp.replace(",","")
                    usa_temp.append(int(gross_temp))
                else:
                    gross_temp = gross_temp.partition(" ")[2]
                    gross_temp = gross_temp.replace(",","")
                    usa_temp.append(int(gross_temp))
            else:
                gross_temp = gross.partition(" ")[2]
                gross_temp = gross_temp.partition(" ")[0]
                gross_temp = gross_temp.replace(",", "")
                other_temp.append(int(gross_temp))
        except:
            # print "ERROR\n", title, "\n", gross
            # logging.exception("logger")
            movies[title]["gross"] = "no_info"

    if len(small_wide_temp) > 0:
        movies[title]["gross"] = max(small_wide_temp)
    elif len(big_wide_temp) > 0:
        movies[title]["gross"] = max(big_wide_temp)
    elif len(usa_temp) > 0:
        movies[title]["gross"] = max(usa_temp)
    elif len(other_temp) > 0:
        movies[title]["gross"] = max(other_temp)
    else:
        movies[title]["gross"] = "no_info"

    small_wide_temp = []
    big_wide_temp = []
    usa_temp = []
    other_temp = []

budget_temp = []
for title in movies:
    budgetes = movies[title]["budget"]
    if budgetes == "no_info":
        rejectes_movies.append([title, "on_budg"])
        pass
    elif len(budgetes) >= 1:
        # print "UNCOORREC", title, budgetes
        for bud in budgetes:
            if bud != "":
                bud_temp = bud.partition(" ")[2]
                bud_temp = bud_temp.partition(" ")[0]
                bud_temp = bud_temp.replace(",","")
                bud_temp = bud_temp.replace(" ","")
                budget_temp.append(int(bud_temp))
        if len(budget_temp) <= 0:
            movies[title]["budget"] = "no_info"
        else:
            movies[title]["budget"] = max(budget_temp)
        # print "COORECTED", title, max(budget_temp)
        budget_temp = []

del business_raw, business_less_raw, movies_with_values, budget_temp, gross_temp, temp

print len(movies), "amount of movies that have stated business values"
######################################################
#                top actors filtering
######################################################

top_actors = {}

with open("IMDB_files_link/_filtered_data/actors.scrapped") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for rank, name in enumerate(reader):
        _name = name[0]
        if _name not in top_actors:
            top_actors[_name] = {"rank": rank + 1}

######################################################
#                actors filtering
######################################################

actors_raw = []
with open("IMDB_files_link/_filtered_data/actors.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        actors_raw.append(full_line)

actors_less_raw = []

temp = []
for line in actors_raw:
    if line != "":
        temp.append(line)
    else:
        # only add actors that have roles listed
        if len(temp) > 1:
            actors_less_raw.append(temp)
        temp = []

movie_and_roles = {}

for entry in actors_less_raw:
    actor = entry[0]
    if "," in actor:
        parted = actor.partition(", ")
        # first name then surname
        # if there is (I) or else in name - delete it
        name_with_paranth = parted[2]
        if "(" in name_with_paranth:
            clean_name = name_with_paranth.partition(" (")[0]
            actor = clean_name + " " + parted[0]
        else:
            actor = parted[2] + " " + parted[0]
    for role in entry[1:len(entry)]:
        movie_name = role.partition("  ")[0]
        if movie_name not in movie_and_roles:
            movie_and_roles[movie_name] = {"cast":[{"actor":actor,"sex": "M"}]}
        else:
            movie_and_roles[movie_name]["cast"].append({"actor":actor,"sex": "M"})

actors_raw = []
with open("IMDB_files_link/_filtered_data/actresses.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        actors_raw.append(full_line)

actors_less_raw = []

temp = []
for line in actors_raw:
    if line != "":
        temp.append(line)
    else:
        # only add actors that have roles listed
        if len(temp) > 1:
            actors_less_raw.append(temp)
        temp = []

for entry in actors_less_raw:
    actor = entry[0]
    if "," in actor:
        parted = actor.partition(", ")
        # first name then surname
        actor = parted[2] + " " + parted[0]
    for role in entry[1:len(entry)]:
        movie_name = role.partition("  ")[0]
        if movie_name not in movie_and_roles:
            movie_and_roles[movie_name] = {"cast":[{"actor":actor,"sex": "F"}]}
        else:
            movie_and_roles[movie_name]["cast"].append({"actor":actor,"sex": "F"})

del actors_less_raw, actors_raw, temp

######################################################
#            actors ranking and adding
######################################################

for title in movie_and_roles:
    if title in movies:
        movies[title].update({"cast": movie_and_roles[title]["cast"]})

print movies["Six-String Samurai (1998)"]

for title in movies.keys():
    if "cast" not in movies[title]:
        movies.pop(title, None)
        rejectes_movies.append([title,"on_cast_no_cast"])
    else:
        if len(movies[title]["cast"]) < actors_amount:
            movies.pop(title, None)
            rejectes_movies.append([title, "on_cast_<_6"])

print len(movies), "amount of movies that have cast specified and with cast bigger then", actors_amount," actors"

top_cast = []

for title in movies:
    cast = movies[title]["cast"]
    if len(cast) >= actors_amount:
        for actor_entry in cast:
            actor = actor_entry["actor"]
            if actor in top_actors:
                rank = top_actors[actor]["rank"]
                top_cast.append({"actor": actor, "rank": rank, "sex": actor_entry["sex"]})
        movies[title]["cast"] = top_cast
        top_cast=[]

for title in movies:
    cast = movies[title]["cast"]
    cast_sorted = sorted(cast, key=lambda k: k['rank'])
    cast_sorted = cast_sorted[:actors_amount]
    # if len(cast_sorted) == 0: print title
    # print cast_sorted
    movies[title]["cast"] = cast_sorted

print movies["Six-String Samurai (1998)"]

for title in movies.keys():
    if len(movies[title]["cast"]) < actors_amount:
        movies.pop(title, None)
        rejectes_movies.append([title, "on_cast_<_6_2"])

print len(movies), "amount of movies after adding cast and with", actors_amount,"actors listed in top list"

del top_cast, top_actors, movie_and_roles
######################################################
#                   plot adding
######################################################

plot_raw = []

with open("IMDB_files_link/_filtered_data/plot.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        plot_raw.append(full_line)

plot_less_raw = []
temp = []
for line in plot_raw:
    if line != "----":
        temp.append(line)
    else:
        temp.append("BY")
        plot_less_raw.append(temp)
        temp = []

movie_plots = {}
one_plot = []
for entry in plot_less_raw:
    for line in entry:
        if "MV" in line:
            title = line.partition("MV: ")[2]
        if "PL" in line:
            one_plot.append(line.partition("PL: ")[2])
        if "BY" in line:
            movie_plots[title] = {"plot": " ".join(one_plot)}
            one_plot = []
            break

for title in movies:
    if title in movie_plots:
        movies[title].update({"plot": movie_plots[title]["plot"]})
    else:
        # print "no plot for:", title
        movies[title].update({"plot": "no_info"})
        rejectes_movies.append([title, "on_plot"])

del movie_plots, one_plot, plot_less_raw, plot_raw

######################################################
#                   runtime adding
######################################################

runtimes = {}

with open("IMDB_files_link/_filtered_data/running-times.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        runtime = parted[2].replace("\t","")
        if ":" in runtime:
            runtime = runtime.partition(":")[2]
        if "(" in runtime:
            runtime = runtime.partition("(")[0]
        runtimes[title] = {"runtime": runtime}

for title in movies:
    if title in runtimes:
        movies[title].update({"run-time": runtimes[title]["runtime"]})
    else:
        # print "no runtime for:", title
        movies[title].update({"run-time": "no_info"})

# add video game filtering - only CoD: Modern Warfare 2

for title in movies.keys():
    if "(VG)" in title:
        movies.pop(title, None)

print len(movies), "amount of movies after removing successful video games"


fsl.save_to_file(movies,actors_amount)

f = open('files/_rejected.movies','w')
for entry in rejectes_movies:
    f.write(str(entry)+"\n")
f.close()