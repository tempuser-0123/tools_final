import wikipedia, unicodedata
import file_save_load as fsl
import time


fileName = 'imdb_dataset_v7_no_plots'
actors_amount = 6

movies = fsl.read_from_file(fileName, actors_amount)

def compute_jaccard_index(list_1, list_2):
    list_1 = list_1.replace("(","").replace(")","")
    list_2 = list_2.replace("(","").replace(")","")
    set_1 = set(list_1.split())
    set_2 = set(list_2.split())
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2)))

movies_with_no_plot = []
wiki_no_plot = []
wiki_plot_ok = []

for title in movies:
    if movies[title]["plot"] == "no_info":
        full_title = title
        title_no_year = title.partition("(")[0]
        movies_with_no_plot.append([title_no_year, full_title])
print "movies with no plot:" , len(movies_with_no_plot)
counter = 0
# TODO Remove limits
# f = open('files/_additional_plot_from_wiki','a',0)

for title in movies_with_no_plot:

    title_no_year = title[0]
    full_title = title[1]
    title_film = str(title_no_year + "(film)")
    year = title[1].partition("(")[2]
    year = year.replace("(","")
    year = year.replace(")","")
    try:
        search_results = wikipedia.search(title_film)
    except:
        print "Error on search_results"
        search_results =[]
        current_query = "no_results"

    search_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in search_results]

    print "search_results for\t", title_film, "\t\t" ,search_results

    for result in search_results:
        if compute_jaccard_index(title_film,result) >= 1:
            current_query = result
            break
        elif compute_jaccard_index(title_no_year,result) >=1:
            current_query = result
            break
        elif compute_jaccard_index(str(title_no_year + " (" + year + " film" + ")"),result) >=1:
            current_query = result
            break
        else:
            current_query = "no_results"

    print "current_query:\t\t", current_query , "/ for movie: ", full_title

    if current_query != "no_results":
        try:
            movie_page = wikipedia.page(current_query)
            go_flag = True
        except:
            print "PLOT------DisambiguationError for:", full_title
            go_flag = False

        if go_flag:
            section_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in movie_page.sections]
            print "sections for\t\t", current_query, section_results, "\n"
            if "Plot" in section_results:
                try:
                    wiki_plot_ok.append([movie_page.section("Plot").replace("\n"," "),full_title])
                except:
                    print "NoneTpye error"

    else:
        wiki_no_plot.append(["no_info_query", full_title])

    counter += 1
    print "Done with:",counter,"/",len(movies_with_no_plot)


print "PLOT:\tmovies with info:", len(wiki_plot_ok), "\tmovies no info:", len(wiki_no_plot), "\tall movies with no info:", len(movies_with_no_plot)

f = open('files/_wiki_plot_for_' + fileName,'w')
f.write(str(time.strftime("%c")) + "\n")
f.write("PLOT:\tmovies with info:" + str(len(wiki_plot_ok)) + "\tmovies no info:" + str(len(wiki_no_plot)) + "\tall movies with no info:" + str(len(movies_with_no_plot)) + "\n")

for entry in wiki_plot_ok:
    f.write(str(entry)+"\n")

f.close()

