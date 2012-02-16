# -*- coding: utf-8 -*-
import pymongo
import bson

import searchers.searcher as searcher

class CoOccurrence(searcher.Searcher):
    """
    Calculates Co-Occurrence of terms in the Document index and uses that for
    the basis of a similarity measure.

    >>> [(x['document']['title'], x['score'])
    ... for x in more_like_this.CoOccurrence().search('4f3d4e8c8e80350dd6000000')]
    """
    def search(self, document_id, offset=0, limit=10):
        """
        Executes a search looking for documents that are similar to the provided
        document_id
        """
        tokens = self.document_storage.find_one(
            bson.objectid.ObjectId(document_id))['terms']

        map_function = bson.Code(
            "function () {"
            "  this.matches.forEach(function(match) {"
            "    if (match.doc_id != doc_id) {"
            "      emit(match.doc_id, {count: match.term_fq});"
            "    }"
            "  });"
            "}")

        reduce_function = bson.Code(
            "function (key, values) {"
            "  return {count: values.length};"
            "}")

        results = self.collection.map_reduce(
            map_function,
            reduce_function,
            scope=dict(doc_id=document_id),
            query=dict(term={"$in": list(tokens)}),
            out=bson.son.SON(dict(inline=1)))

        scored_results = sorted(
            results['results'],
            key=lambda x: x['value']['count'],
            reverse=True)[offset:limit]

        return [
            {'document': self.document_storage.find_one(r['_id']),
             'score': r['value']['count']} for r in scored_results]
