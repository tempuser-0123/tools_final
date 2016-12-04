from bs4 import BeautifulSoup
import unicodedata


def find_all():
    names = []
    for num in range(0,399):
        file = open("IMDB_files_link/imdb_scrap_more_raw_20k/"+str(num))
        soup = BeautifulSoup(file, 'html.parser')
        for table in soup.find_all('table'):
            table_name = str(table.get('class')[0])
            if table_name == "results":
                all_imgs =  table.find_all('img')
                for img in all_imgs:
                    name = img.get('alt')
                    names.append(name)
    all_names_ascii = []
    for name in names:
        all_names_ascii.append(unicodedata.normalize('NFKD', name).encode('ascii', 'ignore'))
    return all_names_ascii

f = open('IMDB_files_link/actors_scrapped_20k','w')
names = find_all()
for name in names:
    f.write(name + "\n")

f.close()