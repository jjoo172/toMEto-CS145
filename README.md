# CS145
CS145 Project Repository - toMEto


To start up toMEto:

Unzip processed.zip (files needed for recipe metadata)
> cd src/backend/data/
> unzip -q processed.zip

Run with default algorithm (weighted PMI)
> cd src/
> python app.py backend/analyzers/analyzer_PMI3.txt

You're done!
Access toMEto locally at 'localhost:5000' (type into browser)
There will be no images since it's about ~3GB total
