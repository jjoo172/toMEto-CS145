CS145 - toMEto
=======

To start up toMEto:
-----------

1. Unzip processed.zip (files needed for recipe metadata)
    * cd src/backend/data/
    * unzip -q processed.zip

2. Run with default algorithm (weighted PMI)
    * cd src/
    * python app.py backend/analyzers/analyzer_PMI3.txt

3. You're done!

4. Access toMEto locally at 'localhost:5000' (type into browser). Note that there will be no images... they take up about ~3GB total so it's not in the repository.
