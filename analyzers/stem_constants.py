# Some exceptional forms not handled.
exceptional_early_exit_post_1a = frozenset(['inning', 'outing', 'canning', 'herring',
                                            'earring', 'proceed', 'exceed', 'succeed'])

doubles = ('bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt')
s1b_suffixes = ('ed', 'edly', 'ing', 'ingly')

s2_triples = (('ization', 'ize', []),
               ('ational', 'ate', []),
               ('fulness', 'ful', []),
               ('ousness', 'ous', []),
               ('iveness', 'ive', []),
               ('tional', 'tion', []),
               ('biliti', 'ble', []),
               ('lessli', 'less', []),
               ('entli', 'ent', []),
               ('ation', 'ate', []),
               ('alism', 'al', []),
               ('aliti', 'al', []),
               ('ousli', 'ous', []),
               ('iviti', 'ive', []),
               ('fulli', 'ful', []),
               ('enci', 'ence', []),
               ('anci', 'ance', []),
               ('abli', 'able', []),
               ('izer', 'ize', []),
               ('ator', 'ate', []),
               ('alli', 'al', []),
               ('bli', 'ble', []),
               ('ogi', 'og', ['l']),
               ('li', '', ['c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't']))

exceptional_forms = {'skis': 'ski',
                    'skies': 'sky',
                    'dying': 'die',
                    'lying': 'lie',
                    'tying': 'tie',
                    'idly': 'idl',
                    'gently': 'gentl',
                    'ugly': 'ugli',
                    'early': 'earli',
                    'only': 'onli',
                    'singly': 'singl',
                    'sky': 'sky',
                    'news': 'news',
                    'howe': 'howe',
                    'atlas': 'atlas',
                    'cosmos': 'cosmos',
                    'bias': 'bias',
                    'andes': 'andes'}

s3_triples = (('ational', 'ate', False),
               ('tional', 'tion', False),
               ('alize', 'al', False),
               ('icate', 'ic', False),
               ('iciti', 'ic', False),
               ('ative', '', True),
               ('ical', 'ic', False),
               ('ness', '', False),
               ('ful', '', False))

s4_delete_list = ('al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement',
                  'ment', 'ent', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize')
