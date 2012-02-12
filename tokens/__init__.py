# -*- coding: utf-8 -*-
import re

WHITESPACE = re.compile(r'\W+')

def whitespace_tokenizer(field_text):
    """
    takes a string of unicode and produces a set of tokens
    """
    return WHITESPACE.sub(' ',field_text.lower()).split()
    
