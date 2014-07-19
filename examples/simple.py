#!/usr/bin/env python2
#coding=utf-8
from os import path
from . import easywordcloud

d = path.dirname(__file__)

width = 960
height = 800
best_elements = None
best_score = 0

text = open(path.join(d, 'constitution.txt')).read()
# Separate into a list of (word, frequency).
words = easywordcloud.process_text(text)
easywordcloud.draw_word_cloud(words, width, height, path.join(d, 'constitution.png'), None)
