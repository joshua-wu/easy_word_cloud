easy_word_cloud
==========
##features
Based on [word_cloud] and [word cloud generate], I created this easy word cloud. 
1. easy to use. compare to word cloud, easy_word_cloud provide a simplier interface.
2. more effcient. compare to word_cloud, easy_word_cloud is more effcient with bigger canvas.
3. custom weight. for each word, the user can provide a weight( a weight can be the count of that word, or the percentage and so on ). the weight must greate than zeros. and there are no other constraint. so you can scale the weight to log scale 
you can provide log(count) as a weight.
4. font size is liner with weight. In order to provide a more reasonable figure, the weight is liner with the font size. 
5. smart draw. to choice font size smart with regard to the size of word, weight of word, size of the canvas. 

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

Install the package:

    sudo python setup.py install

##How to draw a word cloud?
prepare the a list of word tuples. and then call the function
⋅⋅* English
```python
text = open(path.join(d, 'examples/constitution.txt')).read()
words = easywordcloud.process_text(text)
easywordcloud.draw_word_cloud(words, width, height, 'examples/constitution.png')
```
output:
![American Constitution](examples/constitution.png)

```python
text = open(path.join(d, 'examples/alice.txt')).read()
words = easywordcloud.process_text(text)
easywordcloud.draw_word_cloud(words, width, height,  'examples/alice.png', '/Library/Fonts/Andale Mono.ttf')
```
output:
![Alice in Wonderland](examples/alice.png)

⋅⋅* Chinese:
```python
words = [(u'标签', 3), (u'云', 2)]
easywordcloud.draw_word_cloud(words, width, height,  'examples/chinese.png', None)
```
output:
![Chinese](examples/chinese.png)

⋅⋅* Japanness
```python
words = [(u'ワード', 0.7), (u'クラウド', 0.6)]
easywordcloud.draw_word_cloud(words, width, height, 'examples/japanese.png', None)
```
output:
![japanese](examples/japanese.png)

NOTE: **MAKE SURE THE FONT COVERS THE CHARACTERS YOU WANT TO DISPLAY**

Note that if you are not on mac, you need to adjust FONT_PATH to point to
some existing font.

Check out [examples/simple.py][simple] for a short intro. 

[simple]: examples/simple.py
  
