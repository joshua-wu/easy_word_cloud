# Author: Andreas Christian Mueller <amueller@ais.uni-bonn.de>
# (c) 2012
# Modified by: Paul Nechifor <paul@nechifor.net>
#
# License: MIT
#modified by wujian
import os
import re
from .layout_cloud import *


STOPWORDS = set([x.strip() for x in open(os.path.join(os.path.dirname(__file__),
                                                      'stopwords')).read().split('\n')])


def process_text(text, max_features=200, stopwords=None):
    """Splits a long text into words, eliminates the stopwords and returns
    (words, counts) which is necessary for make_wordcloud().

    Parameters
    ----------
    text : string
        The text to be processed.
    
    max_features : number (default=200)
        The maximum number of words.
        
    stopwords : set of strings
        The words that will be eliminated.
        
    Notes
    -----
    There are better ways to do word tokenization, but I don't want to include
    all those things.
    """
    
    if stopwords is None:
        stopwords = STOPWORDS
    
    d = {}
    for word in re.findall(r"\w[\w']*", text):
        word_lower = word.lower()
        if word_lower in stopwords:
            continue

        # Look in lowercase dict.
        if word_lower in d:
            d2 = d[word_lower]
        else:
            d2 = {}
            d[word_lower] = d2

        # Look in any case dict.
        if word in d2:
            d2[word] += 1
        else:
            d2[word] = 1

    d3 = {}
    for d2 in d.values():
        # Get the most popular case.
        first = sorted(d2.items(), key=lambda x: x[1], reverse=True)[0][0]
        d3[first] = sum(d2.values())

    words = sorted(d3.items(), key=lambda x: x[1], reverse=True)
    words = words[:max_features]
    maximum = float(max(d3.values()))
    for i, (word, count) in enumerate(words):
        words[i] = word, count/maximum

    return words
