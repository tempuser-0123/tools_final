import urllib2, time
from random import randint

for req in range(1,20001,50):

    response = urllib2.urlopen('http://www.imdb.com/search/name?gender=male,female&start='+str(req))
    html = response.read()
    with open("IMDB_files_link/imdb_scrap_more_raw_20k/"+str((req-1)/50), "w") as text_file:
        text_file.write(html)
    print "file",(req-1)/50 ,"/400 done"
    # random delay so we wont get [Errno 104] Connection reset by peer
    # which basically means that server thinks we are a bot.. well we are
    time.sleep(randint(10,20))

