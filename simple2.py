#!/usr/bin/env python2
#coding=utf-8
from os import path
import easywordcloud

d = path.dirname(__file__)

width = 800
height = 600
best_elements = None
best_score = 0

#test case 2
text = open(path.join(d, 'examples/constitution.txt')).read()
words = easywordcloud.process_text(text)
easywordcloud.draw_word_cloud(words, width, height, path.join(d, 'examples/constitution.png'))


#test case 2
text = open(path.join(d, 'examples/alice.txt')).read()
words = easywordcloud.process_text(text)
easywordcloud.draw_word_cloud(words, width, height, path.join(d, 'examples/alice.png'), None)

#test case 3
words = [(u'ワード', 0.7), (u'クラウド', 0.6)]
easywordcloud.draw_word_cloud(words, width, height, path.join(d, 'examples/japanese.png'), '/Library/Fonts/Andale Mono.ttf')


words = [(u'标签', 3), (u'云', 2)]
easywordcloud.draw_word_cloud(words, width, height, path.join(d, 'examples/chinese.png'))
