easy_word_cloud
==========
##Features
Based on [word_cloud](https://github.com/amueller/word_cloud) and [word cloud generate](http://www.jasondavies.com/wordcloud/), I created this easy word cloud. 

1. **Super easy to user**. Compared to word cloud, easy_word_cloud provide a simplier interface and you do not need to have cython.
2. **More effcient**. Easy_word_cloud is more effcient with bigger canvas or a plenty of words.
3. **Using weight instead of count**. You can set the weiht to whatever you want( e.g. the count of word, log(count of word) ) only if you ensure it great than 0.
4. **font size is strict liner with weight**. In order to provide a more reasonable figure, the weight is liner with the font size. In [word_cloud](https://github.com/amueller/word_cloud), the size of two words are not compareable because it doest not maintain the linearity.  
5. **Smart draw**. I design a algorithm to smart choice font size with regard to the size of word, weight distribution of word and size of the canvas. 
6. **Unicode and python2/3 support**.


## Installation

Fast install:

    sudo pip install git+git://github.com/knightwu/easy_word_cloud.git

Otherwise, get this package:
    
    wget https://github.com/knightwu/easy_word_cloud/archive/master.zip
    unzip master.zip
    rm master.zip
    cd easy_word_cloud-master

Install the requirements:

    sudo pip install -r requirements.txt
If you are a windows user, you can download the package needed from [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

Install the package:

    sudo python setup.py install

##How to draw a word cloud?
prepare the a list of word tuples. and then call the function

**English**
```python
text = open(path.join(d, 'examples/constitution.txt')).read()
words = easywordcloud.process_text(text)
# to makes the weight more even
words = [(word, math.sqrt(weight)) for word, weight in words]  
easywordcloud.draw_word_cloud(words, width, height, 'examples/constitution.png')
```
output:
![American Constitution](examples/constitution.png)

**Englih with font *Andale Mono***
```python
text = open(path.join(d, 'examples/alice.txt')).read()
words = easywordcloud.process_text(text)
easywordcloud.draw_word_cloud(words, width, height, 
                              'examples/alice.png', 
                              '/Library/Fonts/Andale Mono.ttf')
```
output:
![Alice in Wonderland](examples/alice.png)

**Chinese**
```python
words = [(u'标签', 3), (u'云', 2)]
easywordcloud.draw_word_cloud(words, width, height,  'examples/chinese.png', None)
```
output:
![Chinese](examples/chinese.png)

**Japanness**
```python
words = [(u'ワード', 0.7), (u'クラウド', 0.6)]
easywordcloud.draw_word_cloud(words, width, height, 'examples/japanese.png', None)
```
output:
![japanese](examples/japanese.png)

NOTE: **MAKE SURE THE FONT COVERS THE CHARACTERS YOU WANT TO DISPLAY**
If you are not on mac, you need to adjust FONT_PATH to point to
some existing font.

Check out [examples/simple.py][simple] for a short intro. 

[simple]: examples/simple.py

  
