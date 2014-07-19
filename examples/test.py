#encoding=utf-8
import Image
import ImageDraw
import numpy as np




import Image
import ImageFont, ImageDraw
image=Image.new("RGB",[320,320])
draw = ImageDraw.Draw(image)
a=u"ひらがな - Hiragana, 히라가나"
a = u'你好么？'
font=ImageFont.truetype("/Library/Fonts/hei.ttf",14)
draw.text((50, 50), a, font=font)
image.show()
exit(0)

img = Image.new( 'L', (255,255), "black")  #create a new black image
pixels = img.load()  #create the pixel map
print(pixels)
draw = ImageDraw.Draw(img)
draw.text((0, 0), 'hello')
for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        pixels[i, j] = 100   # set the colour accordingly
        print(pixels[i, j]),
    print('\n'),



print( pixels.any() )
#img.show()


# def binary_search_max(a):
#     '''return the index of the max one'''
#     if len(a) == 0:
#         return -1

#     l, r = 0, len(a)
#     while l < r:
#         m = (l + r) // 2
#         if a[m] > a[l]:
#             r = m
#         elif a[m] 
#     return l



# a = [1,3,7,8]
#to find the max from the binary search

