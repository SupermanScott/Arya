# -*- coding: utf-8 -*-
import pymongo
import bson
import tokens
import analyzers

class Searcher(object):
    """
    Executes a search on the mongo db store and returns the matching mongodb documents
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

    def search(self, query, offest=0, limit=10):
        """
        Executes basic query against index across all searchable text fields
        """
        terms = set()
        for token in self.tokenizer(query):
            for analyzer in self.analyzers:
                token = analyzer(token)
            terms.add(token)

        map_function = bson.Code(
            "function () {"
            "  for (var i=0; i < this.matches.length; i++) {"
            "    var match = this.matches[i];"
            "    var data = {tf: match.term_fq, df: this.document_fq};"
            "    emit(this.matches[i], data);"
            "  }}")

        reduce_function = bson.Code(
            "function (key, values) {"
            "  var result = { tf: 0, df: 0};"
            "  values.forEach(function(value) {"
            "    result.tf += value.tf;"
            "    result.df = value.df;"
            "  });"
            "  return result;"
            "}")

        finalize_function = bson.Code(
            "function (key, value) {"
            "  var score = value.tf * Math.log(total / value.df);"
            "  return value.df;"
            "}")

        total = self.document_storage.count()

        scope = dict(total=total)

        results = self.collection.map_reduce(
            map_function,
            reduce_function,
            finalize=finalize_function,
            scope=scope,
            query={'term': { '$in': list(terms)}},
            out=bson.son.SON(dict(inline=1)))
        return results['results']

