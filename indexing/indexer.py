# -*- coding: utf-8 -*-
import readability.readability as readability
import urllib
import re
import pymongo

# Probably should leverage lxml or BS to really strip tags to get the text
STRIP_HTML = re.compile(r'<[^<]*?/?>')

class DocumentFetcher(object):
    """
    Maps a given url to a dictionary of fields and raw text
    """
    def __init__(self, url):
        self.url = url
        self._document = None

    def get_title(self):
        """
        Returns the title for the document
        """
        return self.document.short_title()

    title = property(get_title, "Title of the url document")

    def get_summary(self):
        """
        Returns the summary for the document
        """
        return STRIP_HTML.sub(' ', self.document.summary())

    summary = property(get_summary, "Summary of the url document")

    def get_content(self):
        """
        Returns the content for the document
        """
        return STRIP_HTML.sub(' ', self.document.content())

    content = property(get_content, "Plain text content of the url document")

    def get_document(self):
        """
        Make the url call and download the document
        """
        if not self._document:
            html = urllib.urlopen(self.url).read()
            self._document = readability.Document(html)
        return self._document

    document = property(get_document, "Document at the provided url")

    def to_dictionary(self):
        """
        Returns itself as a dictionary
        """
        return dict(
            url=self.url,
            title=self.title,
            summary=self.summary,
            content=self.content,
            )

class Indexer(object):
    """
    Defines how to save the documents to Mongo
    """

    def __init__(self, server='localhost', port=27017, database_name='arya',
                 collection_name='index'):
        """
        Connect to mongo and connect to the proper collection.
        """
        connection = pymongo.Connection(server, port)
        self.collection = connection[database_name][collection_name]

        # @TODO provide a way to add a config object for how the fields are
        # tokenized etc.

    def add_document(self, document):
        """
        Adds a document to the search index.
        """
        doc = dict(document)
        print document

    def index_url(self, url):
        """
        Index a provided url
        """
        self.add_document(DocumentFetcher(url).to_dictionary())
