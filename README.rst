==========================================
Arya - Web search prototype built on Mongo
==========================================

--------
Overview
--------
This project was a way to explore Mongodb a bit and its Map Reduce system. Seemed like a fun project and it is far from complete or really that interesting. It has a basic Indexer that, given a url creates a document in Mongo and then indexes the content of the page and makes it searchable. The search provides a simple interface to run the query.

-------
Install
-------
Download, install and run Mongodb
http://www.mongodb.org/downloads

pip install -r requirements.txt


With that installed you are now ready to interact with it via the python console

>>> import indexing.indexer as indexer
>>> import searchers.searcher as s
>>> idx = indexer.Indexer()
>>> idx.index_url('http://www.mongodb.org/display/DOCS/Philosophy')
>>> idx.index_url('http://www.mongodb.org/display/DOCS/Use+Cases')
>>> [(x['document']['title'], x['score']) for x in s.Searcher().search('cloud')]
>>> [(x['document']['title'], x['score']) for x in s.Searcher().search('database power')]


