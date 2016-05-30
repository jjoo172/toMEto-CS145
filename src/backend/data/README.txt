This directory stores all data related files. All the processing has already 
been done, just extract 'processed.zip' to 'processed/'.



If, for any reason, you want to regenerate 'processed/':

1. Run scraper.py to scrape recipes. This requires preloading a few recipe_ids.
2. Run nyt_parser.py to parse the scraped HTML.
3. Run nyt_mapper.py to find the top ingredients and generate a good mapping.
4. Copy all contents of 'nyt_processed/' into 'processed/'.
5. (Optional) Supplement with Allrecipes data.


Supplementing with Allrecipes data:

1. Run scraper.py to scrape recipes (modify the URLs).
2. Run allrecipes_parser.py to parse the scraped HTML.
3. Copy all contents of 'allrecipes_processed/' into 'processed/'.
