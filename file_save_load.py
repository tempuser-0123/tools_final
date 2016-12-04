import time, csv
import unicodedata

def save_to_file(movies, actors_amount):

    timestamp = str(time.strftime("%Y%m%d-%H%M%S"))

    if  actors_amount == 6:
        f = open('files/datasetV_' + timestamp, 'w')

        f.write("title\t" +
                "director\t" +
                "rating\t" +
                "votes\t" +
                "year\t" +
                "genre\t" +
                "gross\t" +
                "budget\t" +
                "run-time\t" +
                "actor1\t" +
                "actor1_rank\t"
                "actor1_sex\t"
                "actor2\t" +
                "actor2_rank\t" +
                "actor2_sex\t" +
                "actor3\t" +
                "actor3_rank\t" +
                "actor3_sex\t" +
                "actor4\t" +
                "actor4_rank\t" +
                "actor4_sex\t" +
                "actor5\t" +
                "actor5_rank\t" +
                "actor5_sex\t" +
                "actor6\t" +
                "actor6_rank\t" +
                "actor6_sex\t" +
                "plot" + "\n"
                )
        for title in movies:
            entry = movies[title]
            f.write(title + "\t" +
                    str(entry["director"]) + "\t" +
                    str(entry["rating"]) + "\t" +
                    str(entry["votes"]) + "\t" +
                    str(entry["year"]) + "\t" +
                    str(entry["genre"]) + "\t" +
                    str(entry["gross"]) + "\t" +
                    str(entry["budget"]) + "\t" +
                    str(entry["run-time"]) + "\t" +
                    str(entry["cast"][0]["actor"]) + "\t" +
                    str(entry["cast"][0]["rank"]) + "\t" +
                    str(entry["cast"][0]["sex"]) + "\t" +
                    str(entry["cast"][1]["actor"]) + "\t" +
                    str(entry["cast"][1]["rank"]) + "\t" +
                    str(entry["cast"][1]["sex"]) + "\t" +
                    str(entry["cast"][2]["actor"]) + "\t" +
                    str(entry["cast"][2]["rank"]) + "\t" +
                    str(entry["cast"][2]["sex"]) + "\t" +
                    str(entry["cast"][3]["actor"]) + "\t" +
                    str(entry["cast"][3]["rank"]) + "\t" +
                    str(entry["cast"][3]["sex"]) + "\t" +
                    str(entry["cast"][4]["actor"]) + "\t" +
                    str(entry["cast"][4]["rank"]) + "\t" +
                    str(entry["cast"][4]["sex"]) + "\t" +
                    str(entry["cast"][5]["actor"]) + "\t" +
                    str(entry["cast"][5]["rank"]) + "\t" +
                    str(entry["cast"][5]["sex"]) + "\t" +
                    str(entry["plot"]) + "\n")
        f.close()

    if actors_amount == 3:
        f = open('files/datasetV_' + timestamp, 'w')

        f.write("title\t" +
                "director\t" +
                "rating\t" +
                "votes\t" +
                "year\t" +
                "genre\t" +
                "gross\t" +
                "budget\t" +
                "run-time\t" +
                "actor1\t" +
                "actor1_rank\t"
                "actor1_sex\t"
                "actor2\t" +
                "actor2_rank\t" +
                "actor2_sex\t" +
                "actor3\t" +
                "actor3_rank\t" +
                "actor3_sex\t" +
                "plot" + "\n"
                )
        for title in movies:
            entry = movies[title]
            f.write(title + "\t" +
                    str(entry["director"]) + "\t" +
                    str(entry["rating"]) + "\t" +
                    str(entry["votes"]) + "\t" +
                    str(entry["year"]) + "\t" +
                    str(entry["genre"]) + "\t" +
                    str(entry["gross"]) + "\t" +
                    str(entry["budget"]) + "\t" +
                    str(entry["run-time"]) + "\t" +
                    str(entry["cast"][0]["actor"]) + "\t" +
                    str(entry["cast"][0]["rank"]) + "\t" +
                    str(entry["cast"][0]["sex"]) + "\t" +
                    str(entry["cast"][1]["actor"]) + "\t" +
                    str(entry["cast"][1]["rank"]) + "\t" +
                    str(entry["cast"][1]["sex"]) + "\t" +
                    str(entry["cast"][2]["actor"]) + "\t" +
                    str(entry["cast"][2]["rank"]) + "\t" +
                    str(entry["cast"][2]["sex"]) + "\t" +
                    str(entry["plot"]) + "\n")
        f.close()

    print "save to file:", timestamp

def read_from_file(file, actors_amount):

    if actors_amount == 6:

        movies = {}

        with open('files/' + file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for entry in reader:
                movies[
                    entry["title"]
                ] = {
                    "director": entry["director"],
                    "rating": entry["rating"],
                    "votes": entry["votes"],
                    "year": entry["year"],
                    "genre": entry["genre"],
                    "gross": entry["gross"],
                    "budget": entry["budget"],
                    "run-time": entry["run-time"],
                    "actor1": entry["actor1"],
                    "actor1_rank": entry["actor1_rank"],
                    "actor1_sex": entry["actor1_sex"],
                    "actor2": entry["actor2"],
                    "actor2_rank": entry["actor2_rank"],
                    "actor2_sex": entry["actor2_sex"],
                    "actor3": entry["actor3"],
                    "actor3_rank": entry["actor3_rank"],
                    "actor3_sex": entry["actor3_sex"],
                    "actor4": entry["actor4"],
                    "actor4_rank": entry["actor4_rank"],
                    "actor4_sex": entry["actor4_sex"],
                    "actor5": entry["actor5"],
                    "actor5_rank": entry["actor5_rank"],
                    "actor5_sex": entry["actor5_sex"],
                    "actor6": entry["actor6"],
                    "actor6_rank": entry["actor6_rank"],
                    "actor6_sex": entry["actor6_sex"],
                    "plot": entry["plot"]
                }
        return movies

    if actors_amount == 3:

        movies = {}

        with open('files/' + file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for entry in reader:
                movies[
                    entry["title"]
                ] = {
                    "director": entry["director"],
                    "rating": entry["rating"],
                    "votes": entry["votes"],
                    "year": entry["year"],
                    "genre": entry["genre"],
                    "gross": entry["gross"],
                    "budget": entry["budget"],
                    "run-time": entry["run-time"],
                    "actor1": entry["actor1"],
                    "actor1_rank": entry["actor1_rank"],
                    "actor1_sex": entry["actor1_sex"],
                    "actor2": entry["actor2"],
                    "actor2_rank": entry["actor2_rank"],
                    "actor2_sex": entry["actor2_sex"],
                    "actor3": entry["actor3"],
                    "actor3_rank": entry["actor3_rank"],
                    "actor3_sex": entry["actor3_sex"],
                    "plot": entry["plot"]
                }
        return movies

def save_to_dataset(movies, actors_amount):

    timestamp = str(time.strftime("%Y%m%d-%H%M%S"))

    if actors_amount == 6:
        f = open('files/datasetV_' + str(time.strftime("%Y%m%d-%H%M%S")), 'w')

        f.write("title\t" +
                "director\t" +
                "rating\t" +
                "votes\t" +
                "year\t" +
                "genre\t" +
                "gross\t" +
                "budget\t" +
                "run-time\t" +
                "actor1\t" +
                "actor1_rank\t"
                "actor1_sex\t"
                "actor2\t" +
                "actor2_rank\t" +
                "actor2_sex\t" +
                "actor3\t" +
                "actor3_rank\t" +
                "actor3_sex\t" +
                "actor4\t" +
                "actor4_rank\t" +
                "actor4_sex\t" +
                "actor5\t" +
                "actor5_rank\t" +
                "actor5_sex\t" +
                "actor6\t" +
                "actor6_rank\t" +
                "actor6_sex\t" +
                "plot" + "\n"
                )
        for title in movies:
            entry = movies[title]
            f.write(title + "\t" +
                    str(entry["director"]) + "\t" +
                    str(entry["rating"]) + "\t" +
                    str(entry["votes"]) + "\t" +
                    str(entry["year"]) + "\t" +
                    str(entry["genre"]) + "\t" +
                    str(entry["gross"]) + "\t" +
                    str(entry["budget"]) + "\t" +
                    str(entry["run-time"]) + "\t" +
                    str(entry["actor1"]) + "\t" +
                    str(entry["actor1_rank"]) + "\t" +
                    str(entry["actor1_sex"]) + "\t" +
                    str(entry["actor2"]) + "\t" +
                    str(entry["actor2_rank"]) + "\t" +
                    str(entry["actor2_sex"]) + "\t" +
                    str(entry["actor3"]) + "\t" +
                    str(entry["actor3_rank"]) + "\t" +
                    str(entry["actor3_sex"]) + "\t" +
                    str(entry["actor4"]) + "\t" +
                    str(entry["actor4_rank"]) + "\t" +
                    str(entry["actor4_sex"]) + "\t" +
                    str(entry["actor5"]) + "\t" +
                    str(entry["actor5_rank"]) + "\t" +
                    str(entry["actor5_sex"]) + "\t" +
                    str(entry["actor6"]) + "\t" +
                    str(entry["actor6_rank"]) + "\t" +
                    str(entry["actor6_sex"]) + "\t" +
                    str(entry["plot"]) + "\n")
        f.close()

    if actors_amount == 3:
        f = open('files/datasetV_' + str(time.strftime("%Y%m%d-%H%M%S")), 'w')

        f.write("title\t" +
                "director\t" +
                "rating\t" +
                "votes\t" +
                "year\t" +
                "genre\t" +
                "gross\t" +
                "budget\t" +
                "run-time\t" +
                "actor1\t" +
                "actor1_rank\t"
                "actor1_sex\t"
                "actor2\t" +
                "actor2_rank\t" +
                "actor2_sex\t" +
                "actor3\t" +
                "actor3_rank\t" +
                "actor3_sex\t" +
                "plot" + "\n"
                )
        for title in movies:
            entry = movies[title]
            f.write(title + "\t" +
                    str(entry["director"]) + "\t" +
                    str(entry["rating"]) + "\t" +
                    str(entry["votes"]) + "\t" +
                    str(entry["year"]) + "\t" +
                    str(entry["genre"]) + "\t" +
                    str(entry["gross"]) + "\t" +
                    str(entry["budget"]) + "\t" +
                    str(entry["run-time"]) + "\t" +
                    str(entry["actor1"]) + "\t" +
                    str(entry["actor1_rank"]) + "\t" +
                    str(entry["actor1_sex"]) + "\t" +
                    str(entry["actor2"]) + "\t" +
                    str(entry["actor2_rank"]) + "\t" +
                    str(entry["actor2_sex"]) + "\t" +
                    str(entry["actor3"]) + "\t" +
                    str(entry["actor3_rank"]) + "\t" +
                    str(entry["actor3_sex"]) + "\t" +
                    str(entry["plot"]) + "\n")
        f.close()

    print "save to file:", timestamp

def read_from_file_no_plots(file, actors_amount):

    if actors_amount == 6:

        movies = {}

        with open('files/' + file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for entry in reader:
                movies[
                    entry["title"]
                ] = {
                    "director": entry["director"],
                    "rating": entry["rating"],
                    "votes": entry["votes"],
                    "year": entry["year"],
                    "genre": entry["genre"],
                    "gross": entry["gross"],
                    "budget": entry["budget"],
                    "run-time": entry["run-time"],
                    "actor1": entry["actor1"],
                    "actor1_rank": entry["actor1_rank"],
                    "actor1_sex": entry["actor1_sex"],
                    "actor2": entry["actor2"],
                    "actor2_rank": entry["actor2_rank"],
                    "actor2_sex": entry["actor2_sex"],
                    "actor3": entry["actor3"],
                    "actor3_rank": entry["actor3_rank"],
                    "actor3_sex": entry["actor3_sex"],
                    "actor4": entry["actor4"],
                    "actor4_rank": entry["actor4_rank"],
                    "actor4_sex": entry["actor4_sex"],
                    "actor5": entry["actor5"],
                    "actor5_rank": entry["actor5_rank"],
                    "actor5_sex": entry["actor5_sex"],
                    "actor6": entry["actor6"],
                    "actor6_rank": entry["actor6_rank"],
                    "actor6_sex": entry["actor6_sex"]
                }
        return movies

    if actors_amount == 3:

        movies = {}

        with open('files/' + file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for entry in reader:
                movies[
                    entry["title"]
                ] = {
                    "director": entry["director"],
                    "rating": entry["rating"],
                    "votes": entry["votes"],
                    "year": entry["year"],
                    "genre": entry["genre"],
                    "gross": entry["gross"],
                    "budget": entry["budget"],
                    "run-time": entry["run-time"],
                    "actor1": entry["actor1"],
                    "actor1_rank": entry["actor1_rank"],
                    "actor1_sex": entry["actor1_sex"],
                    "actor2": entry["actor2"],
                    "actor2_rank": entry["actor2_rank"],
                    "actor2_sex": entry["actor2_sex"],
                    "actor3": entry["actor3"],
                    "actor3_rank": entry["actor3_rank"],
                    "actor3_sex": entry["actor3_sex"]
                }
        return movies


def read_from_file_less(file, actors_amount):

    if actors_amount == 6:

        movies = {}

        with open('files/' + file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for entry in reader:
                movies[
                    entry["title"]
                ] = {
                    "genre": entry["genre"],
                    "gross": entry["gross"],
                    "budget": entry["budget"],
                    "actor1": entry["actor1"],
                    "actor2": entry["actor2"],
                    "actor3": entry["actor3"],
                    "actor4": entry["actor4"],
                    "actor5": entry["actor5"],
                    "actor6": entry["actor6"],
                }
        return movies

    if actors_amount == 3:

        movies = {}

        with open('files/' + file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for entry in reader:
                movies[
                    entry["title"]
                ] = {
                    "genre": entry["genre"],
                    "gross": float(entry["gross"]),
                    "budget": float(entry["budget"]),
                    "actor1": entry["actor1"],
                    "actor2": entry["actor2"],
                    "actor3": entry["actor3"],
                }
        return movies