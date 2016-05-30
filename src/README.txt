Running ToMEto as is:
  >> python app.py backend/analyzers/analyzer_*.txt

New analyzer algorithm*:
  >> cd backend/analyzers/
  >> python analyzer_new.py
  >> cd ../..
  >> python app.py analyzer_new.txt


* This requires 'backend/data/processed/' to be populated. All the heavy lifting
has already been done, just extract 'backend/data/processed.zip'.
