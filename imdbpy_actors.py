from imdb import IMDb
import json, requests
import time
from random import randint
import file_save_load as fsl

ia = IMDb()

base_url = "http://www.omdbapi.com/?i=tt"

movies = fsl.read_from_file("imdb_dataset_v6.0.2_3_actors_complete.tsv", 3)
log_file = open('log_file.txt', 'a', 0)


def change_movie_data_3actors(title, new_list):
    try:
        movies[title]["actor1"] = str(new_list[0])
        movies[title]["actor2"] = str(new_list[1])
        movies[title]["actor3"] = str(new_list[2])
    except:
        print "failed converting,", new_list[1]


def timestamp():
    return str(time.strftime("%Y-%m-%d\t%H:%M:%S"))


def logger(*args):
    msg = ""
    for a in args:
        msg += str(a)
    with_timestamp = msg + "\t" + timestamp()
    log_file.write(with_timestamp + "\n")
    print with_timestamp


def format_title(t):
    if "/" in t:
        t = t.partition("/")[0]
        t += ")"
        return t
    return t


logger("------------LOG START ", timestamp(), "------------")

movieID_list = ""
movieID = ""
movie_url = ""
response = ""

failed_movies = []
c = 0

for title in movies:
    try:
        movieID_list = ia.search_movie(format_title(title))
        movieID = movieID_list[0].movieID
        ok = True
    except:
        logger("E1:\t", title, "\tnot found! The list returned:\t", movieID_list)
        failed_movies.append(title)
        ok = False

    if ok:
        try:
            movie_url = base_url + str(movieID)
            response = requests.get(movie_url)
            movie_info = json.loads(response.text)
            actors_converted = [a.encode("latin-1") for a in movie_info['Actors'].split(',')]
            if len(actors_converted) >= 3:
                change_movie_data_3actors(title, actors_converted[:3])
                logger("OK\t", title, "\tactors:\t",str(actors_converted),"\t", c, "/", len(movies))
            else:
                logger("E2\t", title, "\tactors:\t",str(actors_converted),"\t", c, "/", len(movies))
        except:
            logger("E3:\t", title, "\twhile getting movieID:\t", movieID, "\tURL:", movie_url, "\tresponse:\t", str(response))
            failed_movies.append(title)

    movieID_list = ""
    movieID = ""
    movie_url = ""
    response = ""
    time.sleep(randint(3, 8))
    c += 1



logger("----FAILED MOVIES----")
for title in failed_movies:
    logger(title)

fsl.save_to_dataset(movies, 3)