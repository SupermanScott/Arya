# -*- coding: utf-8 -*-
import readability.readability as readability
import urllib
import re
import pymongo

import tokens
import analyzers

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
                 collection_name='index', document_storage='docs'):
        """
        Connect to mongo and connect to the proper collection.
        """
        connection = pymongo.Connection(server, port)
        self.collection = connection[database_name][collection_name]
        self.document_storage = connection[database_name][document_storage]

        # @TODO provide a way to add a config object for how the fields are
        # tokenized etc.
        # Only one tokenizer
        self.tokenizer = tokens.whitespace_tokenizer
        # Several analyzers. For instance, stemmer, bi grams, stop words...
        self.analyzers = (
            analyzers.porter_stemer,)


        self.text_fields = (
            'title',
            'content',
            )

    def add_document(self, document):
        """
        Adds a document to the search index.
        """
        doc = dict(document)
        is_update = '_id' in doc

        document_id = self.document_storage.save(doc)
        terms_added = set()

        for field_name in self.text_fields:
            processed_tokens = {}
            for token in self.tokenizer(doc.get(field_name, '')):
                original_word = token
                for analyzer in self.analyzers:
                    token = analyzer(token)
                processed_tokens[token] = processed_tokens.get(token, 0) + 1

            for token, frequency in processed_tokens.iteritems():
                match_object = dict(
                    doc_id=document_id,
                    field_name=field_name,
                    original_word=original_word,
                    term_fq=frequency)

                exists = self.collection.find_one(dict(term=token))
                update_match = {}
                if exists and is_update:
                    for match in exists['matches']:
                        # This document is already in the reverse index.
                        if match.get('doc_id', '') == document_id and \
                                match.get('field_name', '') == field_name:
                            # @TODO: Remove this and replace with match_object
                            update_match = match
                            break
                if exists and not is_update:
                    if term not in terms_added:
                        exists['document_fq'] += 1
                    exists['matches'].append(match_object)
                    self.collection.save(exists)

                else:
                    term_document = dict(
                        term=token,
                        matches=[match_object],
                        document_fq=1)
                    self.collection.save(term_document)
                terms_added.add(token)

        # Store the terms_added on the document
        doc['terms'] = list(terms_added)
        self.document_storage.save(doc)

    def index_url(self, url):
        """
        Index a provided url
        """
        document = self.document_storage.find_one(dict(url=url))
        if not document:
            document = DocumentFetcher(url).to_dictionary()
        self.add_document(document)
