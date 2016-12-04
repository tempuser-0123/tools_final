import file_save_load as fsl
import csv
import unicodedata
from unidecode import unidecode
import io

movies = fsl.read_from_file("imdb_dataset_v7.1_6_actors_complete_wrong_genre.tsv", 6)

movies_and_genres = {}

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

        if title not in movies_and_genres:
            movies_and_genres[title] = [genre]
        else:
            movies_and_genres[title].append(genre)

for title in movies:
    try:
        movies[title]["genre"] = movies_and_genres[title][0]
    except:
        print "error", title, type(title)

fsl.save_to_dataset(movies,6)

