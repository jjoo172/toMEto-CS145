""" Handles search queries from the frontend, returning relevant recipe_ids.
"""
import urllib2
import re


def search(query):
    tokenized = query.split(" ")
    url = "http://cooking.nytimes.com/search?q=" + "+".join(tokenized)

    req = urllib2.urlopen(url)
    content = req.read()
    
    pattern = r'data-url="/recipes/(\d+)'

    return re.findall(pattern, content)
