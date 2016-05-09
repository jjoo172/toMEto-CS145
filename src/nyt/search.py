import urllib2
from bs4 import BeautifulSoup


def search(query):
    tokenized = query.split(" ")
    url = "http://cooking.nytimes.com/search?q=" + "+".join(tokenized)

    req = urllib2.urlopen(url)
    content = req.read()

    soup = BeautifulSoup(content, 'html.parser')

    articles_result = soup.find_all('article')

    result_ids = []

    for a in articles_result:
        try:
            result_ids.append(a["data-id"])
        except Exception as e:
            print "Error retrieving some article"
            # this is typically because of a paid post advertisement...


    return result_ids
