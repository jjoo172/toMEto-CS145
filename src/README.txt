Running ToMEto as is:
  >> python app.py nyt/analyzer_*.txt

Use a new analyzer algorithm:
  >> cd nyt
  >> python analyzer_new.py
  >> cd ..
  >> python app.py analyzer_new.txt

Recomputing everything (requires nyt/processed/ directory to be populated):
  >> cd nyt
  >> python mapper.py
  >> python analyzer_*.py
  >> cd ..
  >> python app.py analyzer_*.txt
