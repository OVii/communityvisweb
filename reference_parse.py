"""
 For taxonomy items, we can add references like this {{bibtex_entry_id}}. The defs in this file
 deal with parsing and formatting this text from the database and into the pages.
"""

from web.models import Reference

"""
 Returns a list of tuples denoting the indices of all references (including {{}} brackets)
"""


def indices(meta_str):
    ind = []
    i = 0
    while i < len(meta_str):
        if meta_str[i] == '{' and meta_str[i + 1] == '{':
            'skip ahead to end bracket'
            start = i
            while meta_str[i] != '}' and i < len(meta_str):
                i = i + 1

            print "Indices start: " + str(start) + " and i: " + str(i)
            ref_str = meta_str[start:i]

            ind = ind + [(start, i + 1)]
        else:
            i = i + 1
    return ind


