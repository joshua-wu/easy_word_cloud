# Author: Andreas Christian Mueller <amueller@ais.uni-bonn.de>
# (c) 2012
# Modified by: Paul Nechifor <paul@nechifor.net>
# License: MIT
#Modified by jack wu

import random
import os
import numpy as np
import math
import imp

try:
    imp.find_module('PIL')
    found = True
except ImportError:
    found = False

if found:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
else:
    import Image
    import ImageDraw
    import ImageFont

debug = 0
float_min = 1e-300

from sys import platform as _platform


def get_default_font():
    """return the default font of different operator system,
    highly recommend you prepare the fonts youself instead of using this function"""
    if _platform == "linux" or _platform == "linux2":
        # linux, sorry, i dont know much
        FONT_PATH = '/usr/share/fonts/truetype/droid/DroidSansMono.ttf'
    elif _platform == "darwin":
        # OS X
        FONT_PATH = "/Library/Fonts/hei.ttf"
    elif _platform == "win32":
        # Windows...
        FONT_PATH = "c:/windows/fonts/msyh.ttf"

    return FONT_PATH


def draw_word_cloud(words, width=800, height=600, output_file_name=None, font_path=None):
    """
    Generate the word cloud.

    Parameters
    ----------
    words : array of tuples
        A tuple contains the word and its weight. The weight must greate than 0. the weight can be any positive num.

    width : int (default=800)
        Width of the canvas.

    height : int (default=600)
        Height of the canvas.

    output_file_name: string (default=None)
        the path to the output figure name.
        if the output_file_name is not None, a picture with path output_file_name will be saved.

        if the output_file_name is None. it will Displays an image.
        On Unix platforms, it will saves the image to a temporary PPM file, and calls the xv utility.
        On Windows, it will saves the image to a temporary BMP file, and uses the standard BMP display utility to show it.

    font_path : string
        Font path to the font that will be used (OTF or TTF). If the font_path is None then will
        call the get_default_font to get_default_font
        to get a default font.
    Notes
    -----
    """
    best_score = 0
    best_elements = None

    for font_scale in [0.1, 0.5, 1, 2, 5, 7, 10, 15, 20, 30, 50]:
        elements, score, fill_rate, show_rate = fit_words(
            words, width=width, height=height, margin=2, scale=font_scale)
        if debug >= 1:
            print('scale:', font_scale, 'score:', score, 'show_rate:', show_rate, 'fille_rate:', fill_rate)
        if score > best_score:
            best_elements, best_score = elements, score
        if score == 0.0:
            break

    draw(best_elements, output_file_name, width=width, height=height, scale=1)


def random_color_func(word, font_size, position, orientation):
    return "hsl(%d" % random.randint(0, 255) + ", 80%, 50%)"


def select_orintation(font_size, font_path, canvas_size, word, margin, draw, font):
    """"choice the orintation for each word"""
    width, height = canvas_size

    draw.setfont(font)
    nontransposed_box_size = draw.textsize(word)

    transposed_font = ImageFont.TransposedFont(font, orientation=Image.ROTATE_90)
    draw.setfont(transposed_font)
    transposed_box_size = draw.textsize(word)

    box_size = None
    orientation = None

    if not check_in_bound((width, height), (transposed_box_size[1] + margin, transposed_box_size[0] + margin)):
        box_size = nontransposed_box_size
        orientation = None
    elif not check_in_bound((width, height), (nontransposed_box_size[1] + margin, nontransposed_box_size[0] + margin)):
        box_size = transposed_box_size
        orientation = Image.ROTATE_90

    if debug >= 1:
        print('trans:', transposed_box_size, 'nontrans:', nontransposed_box_size, orientation, box_size)
            # transpose font optionally
    if box_size is None:
        box_size, orientation = random.choice([(nontransposed_box_size, None)]*9 + [(transposed_box_size, Image.ROTATE_90)])

    return box_size, orientation


def fit_words(words, font_path=None, width=80, height=40,
              margin=2, prefer_horiz=0.90, scale=5, file_name=None):
    """Generate the positions for words.

    Parameters
    ----------
    words : array of tuples
        A tuple contains the word and its frequency.

    font_path : string
        Font path to the font that will be used (OTF or TTF).
        Defaults to DroidSansMono path, but you might not have it.

    width : int (default=400)
        Width of the canvas.

    height : int (default=200)
        Height of the canvas.

    margin: int(default=2)

    prefer_horiz : float (default=0.90)
        The ratio of times to try horizontal fitting as opposed to vertical.

    scale : int( default=5)
        this number is used to scale the font size in case of the font is too small.
    Notes
    -----
    """

    if len(words) <= 0:
        print("We need at least 1 word to plot a word cloud, got %d."
              % len(words))

    if font_path is None:
        font_path = get_default_font()

    if not os.path.exists(font_path):
        raise ValueError("The font %s does not exist." % font_path)
    
    # create image
    img_grey = Image.new("L", (width, height))
    draw = ImageDraw.Draw(img_grey)
    valid_words, font_sizes, positions, orientations = [], [], [], []
    
    #sort the words by weight
    sum_weight = sum(weight for word, weight in words)
    words = [(word, weight * 1.0 / sum_weight) for word, weight in words]
    # start drawing grey image
    for word, weight in sorted(words, key=lambda x: x[1], reverse=True):
        # alternative way to set the font size
        integral = np.asarray(img_grey)

        font_size = int((weight * height * scale))
        font = ImageFont.truetype(font_path, font_size)

        box_size, orientation = select_orintation(font_size, font_path, (width, height), word, margin, draw, font)

        # find possible places using integral image:
        result = query_integral_image(integral, (box_size[0] + margin,
                                      box_size[1] + margin))

        if result is None:
            break

        if debug >= 1:
            print('font_size', font_size, word, weight, 'orientation:', orientation, 'pos:', result, 'box_size:', box_size)

        x, y = np.array(result) + margin // 2
        #need to reset the font
        transposed_font = ImageFont.TransposedFont(font, orientation=orientation)
        draw.setfont(transposed_font)
        draw.text((y, x), word, fill="white")
        # store the information
        valid_words.append((word, weight))
        positions.append((x, y))
        orientations.append(orientation)
        font_sizes.append(font_size)

    fill_rate = 1.0 * (integral != 0).sum() / (integral.shape[0] * integral.shape[1])
    show_rate = len(valid_words) * 1.0 / len(words)
    score = show_rate * fill_rate
    if debug >= 3:
        print(zip(valid_words, font_sizes, positions, orientations))
        print('size:', len(valid_words), 'all:', len(words))
    if debug >= 1:
        print('integral sum:', (integral != 0).sum(), 'show_rate:', show_rate, 'fille_rate:', fill_rate, 'score:', score)
    return zip(valid_words, font_sizes, positions, orientations), score, fill_rate, show_rate


def draw(elements, file_name=None, font_path=None, width=80, height=40, scale=1,
         color_func=random_color_func):
    if font_path is None:
        font_path = get_default_font()
        
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for (word, weight), font_size, position, orientation in elements:
        font = ImageFont.truetype(font_path, font_size)
        transposed_font = ImageFont.TransposedFont(font,
                                                   orientation=orientation)
        draw.setfont(transposed_font)
        color = random_color_func(word, font_size * scale, position, orientation)
        pos = (position[1], position[0])
        draw.text(pos, word, fill=color)

    if file_name is not None:
        img.save(file_name)
    else:
        img.show()

    if debug >= 3:
        a = np.asarray(img)
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                print(1 if a[i, j].any() else 0),
            print('\n'),


def collision_detect(integral_image, pos, box_size):
    height, width = integral_image.shape
    x, y = pos
    box_width, box_height = box_size

    #out of the bound
    if x + box_height >= height or y + box_width >= width:
        return True

    if integral_image[x: x + box_height, y: y + box_width].any():
        return True

    return False


def get_spiral_function(size):
    width, height = size
    e = width * 1.0 / height
    return lambda t: (t * 1.0 * math.cos(t), e * t * math.sin(t))


def euclid_distance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def check_in_bound(size, pos_current):
    """check the pos_current in the bound or not """
    pos_x, pos_y = pos_current[0], pos_current[1]
    width, height = size
    if pos_x >= 0 and pos_x < height and pos_y >= 0 and pos_y < width:
        return True

    return False


def query_integral_image(integral_image, box_size):
    #print('sum:', integral_image.sum())
    height = integral_image.shape[0]
    width = integral_image.shape[1]
    box_width, box_height = box_size
    #area, i, j
    spiral = get_spiral_function((width, height))
    delta = random.choice([1, -1])
    t = 0
    #pos_begin_x, pos_begin_y = random.randint(0, height-1), random.randint(0, width-1)
    pos_begin_x, pos_begin_y = \
        int((height - box_height) * random.uniform(0.25, 0.75)), int((width - box_width) * random.uniform(0.25, 0.75))
    
    #print('begin:x:y:', pos_begin_x, pos_begin_y, box_size, (width, height), height - box_height)
    max_distance = euclid_distance((height, width), (0, 0))
    while True:
        #first geenrate a random point on the horizon
        pos_x, pos_y = spiral(t)
        pos_x, pos_y = int(pos_x + pos_begin_x + 0.5), int(pos_y + pos_begin_y + 0.5)
        t += delta

        #then move it piral
        if euclid_distance((pos_x, pos_y), (pos_begin_x, pos_begin_y)) >= max_distance:
            break

        if not check_in_bound((width, height), (pos_x, pos_y)):
            continue

        if not collision_detect(integral_image, (pos_x, pos_y), box_size):
            if debug >= 3:
                for i in range(integral_image.shape[0]):
                    for j in range(integral_image.shape[1]):
                        print(1 if integral_image[i, j] != 0 else 0),
                    print('\n'),
            return pos_x, pos_y

    return None
