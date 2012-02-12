# -*- coding: utf-8 -*-
import indexing.indexer as idx
import feedparser

def main():
    with open('feeds') as feeds:
        f = feeds.readlines()
    uniques = set([u.strip() for u in f])

    indexer = idx.Indexer()
    for feed in uniques:
        try:
            parsed = feedparser.parse(feed)
        except:
            # who cares...
            continue

        for entry in parsed.entries:
            try:
                indexer.index_url(entry.link)
            except:
                # who cares...
                continue

if __name__ == '__main__':
    main()
        

    
