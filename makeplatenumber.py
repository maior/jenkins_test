'''
Author  : Hyoung Geun Kwon
Email   : maiordba@gmail.com
Desc    :
        폰트 및 사이즈에 따라 Dictionary를 참조하여
        아래와 같이 이미지 및 라벨을 생성한다.
        1. 폰트 읽기
        2. Dictionary 읽기
        3. 이미지 생성하기
        4. 라벨링 생성하기
'''
import argparse
import glob
import io
import os
import random

import numpy as np
from PIL import Image, ImageFont, ImageDraw
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import cv2
import matplotlib.image as mpimg

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

#DEFAULT_FONTS_DIR = os.path.join(SCRIPT_PATH, '/Users/maior/Documents/tensorflow/tensorflow-hangul-recognition/fonts')
DEFAULT_FONTS_DIR = os.path.join(SCRIPT_PATH, './fonts')

fonts = glob.glob(os.path.join(DEFAULT_FONTS_DIR, '*.ttf'))
IMAGE_WIDTH = 152
IMAGE_HEIGHT= 152
FONT_SIZE=142
#PADDING=20
PADDING=0
DRAWINGTEXT_PADDING=0

bigfontonly = ['big_noodle_titling', 'Vogue', 'type_writer', 'Moonlightning', 'School_Times', 'Neothic', 
        'BebasNeue-Regular', 'Azonix', 'theboldfont', 'DolceVita' ]

engfontonly = ['Chapaza', 'big_noodle_titling', 'American_Typewriter_Regular', 'Vogue', 'type_writer', 
        'Typo', 'Moonlightning', 'zai_Olivetti-UnderwoodStudio21Typewriter', 'GeosansLight', 'CourierStd-Oblique', 
        'School_Times', 'TypoLatinserif-Bold', 'Roboto-Regular', 'Neothic', 'CourierStd-BoldOblique', 
        'CourierStd-Bold', 'Dosis-Light', 'MADE-Canvas-Regular-PERSONAL-USE', 'Times_New_Roman', 'BebasNeue-Regular',
        'ADega-Serif-Regular', 'Roboto-Condensed', 'ChampagneLimousines', 'BodoniXT', 'CaviarDreams', 'Azonix',
        'CourierStd', 'Quicksand_Light', 'Arial', 'Quicksand_Bold', 'BaltimoreTypewriterBoldBeveled', 'Mont-HeavyDEMO',
        'Old_Typewriter2.0', 'zai_ConsulPolishTypewriter', 'Tox_Typewriter', 'AA_typewriter', 'Rounded_Elegance',
        'Walkway_UltraExpand', 'coolvetica_crammed_rg', 'theboldfont', 'Dosis-ExtraLight', 'DolceVita', 
        'JMH_Typewriter-Bold', 'steelfish_rg', 'coolvetica_condensed_rg', 'JMH_Typewriter', 'Walkway_Condensed']

diction_txt = './platenumber.txt'

with io.open(diction_txt, 'r', encoding='utf-8') as f:
    labels = f.read().splitlines()


def getFitCharHeight(font, character):
    print('getFitCharHeight : {}'.format(character))
    charimage = Image.new('L', (IMAGE_WIDTH, IMAGE_HEIGHT), color=255)
    chardrawing = ImageDraw.Draw(charimage)
    ch_w, ch_h = chardrawing.textsize(character, font=font)
    print(ch_w, ch_h)
    chardrawing.text(
            (DRAWINGTEXT_PADDING, DRAWINGTEXT_PADDING),
            character,
            fill=(0),
            font=font
        )
    img = np.asarray(charimage)
    #print(img)
    #h, w = img.shape
    bBlack = False
    #print(img)
    #print('{}, {}'.format(h, w))
    #print(img.shape)
    img_h = 0

    for i in range(0, ch_h):
        for j in range(0, ch_w):
            #print(img[i][j])
            if img[i][j] != 255:
                #print(img[i][j])
                #print('{}, {}'.format(i, j))
                img_h = i
                bBlack = True
                break

        if bBlack == True:
            break

    return img_h, bBlack

def getImageMaxSize(fontname, font, words):
    #image = Image.new('L', (IMAGE_WIDTH, IMAGE_HEIGHT), color=0)
    image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), (0,0,0))
    drawing = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, FONT_SIZE)

    tw = 0
    mxh = 0
    for character in words:
        w, h = drawing.textsize(character, font=font)
        print(fontname, character, w,h)
        if mxh < h: mxh = h
        tw += w

    #print(tw, mxh)
    return tw, mxh

def makeCharPostionText():
    pass

def saveWordsImage(words, fontname, totalcount):
    print(words)
    img_w, img_h = getImageMaxSize(fontname, fontname, words)

    bgcolorlist = [[255,255,255], 
                [255,0,0], 
                [255,255,0], 
                [0,255,0],
                [0,255,255], 
                [0,0,255],
                [0,0,0],
                [26,65,38],
                [216,171,0]]

    fontcolor = [[0,0,0], [255,255,255]]

    randpickcolor = random.randrange(0,8)
    print(randpickcolor)
    bgcolor = bgcolorlist[randpickcolor]
    print(bgcolor)

    # if it's green, would be font color's white
    if randpickcolor == 4 or randpickcolor == 3 or randpickcolor == 0 or randpickcolor == 8 or randpickcolor==2: 
        txtcolor = fontcolor[0]
    else:
        txtcolor = fontcolor[1]

    print(img_w, img_h)
    #image = Image.new('L', (img_w+PADDING, img_h+PADDING), color=255)
    image = Image.new('RGB', (img_w+PADDING, img_h+PADDING), (bgcolor[0], bgcolor[1], bgcolor[2]))
    drawing = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontname, FONT_SIZE)

    # drawing text
    tw = 0
    minh = 10000

    filename = words
    # save text
    words_string = '{}_{}.txt'.format(filename, totalcount)
    file_path = './fontimage'
    words_text = io.open(os.path.join(file_path, words_string), 'w', encoding='utf-8')

    for character in words:
        boxinfo = ''
        w, h = drawing.textsize(character, font=font)
        drawing.text(
            (tw+DRAWINGTEXT_PADDING, DRAWINGTEXT_PADDING),
            character,
            fill=(txtcolor[0], txtcolor[1], txtcolor[2]),
            font=font
        )
        print(fontname, character, w,h)

        x = 0
        y = 0

        # add x, y postion and character
        ch_h, bBlack = getFitCharHeight(font, character)
        print('ch_h : {}, img_h : {} '.format(ch_h, img_h))
        h = h - ch_h
        #x = tw+5
        x = tw
        y = ch_h
        #print('{} height : {} '.format(character, h))
        #print('top : {}'.format(ch_h))
        #print('y : {}'.format(y))

        #boxinfo = fontname + ',' + str(w) + ',' + str(h) + ',' + str(x) + ',' + str(y) + ',' + str(x+w) + ',' + str(y) + ',' + str(x+w) + ',' + str(y+h) + ',' + str(x) + ',' + str(y+h) + ',' + character
        boxinfo = str(x) + ',' + str(y) + ',' + str(x+w) + ',' + str(y) + ',' + str(x+w) + ',' + str(y+h) + ',' + str(x) + ',' + str(y+h) + ',' + character
        print('----')
        print(boxinfo)
        print('----')
        print('{}, {}, {}, {}'.format(x, y, w, h))
        print('----')

        img = np.asarray(image)
        #cv2.rectangle(img, (x, y, x+w, y+h), (255,0,0))

        if bBlack == True:
            if ch_h < minh: minh = ch_h

        tw += w

        # Space is excepted
        if character == ' ':
            continue

        words_text.write(u'{}\n'.format(boxinfo))

    words_text.close()
    print(tw, minh)

    #file_string = '{}_{}.jpg'.format(words, totalcount)
    file_string = '{}_{}.jpg'.format(filename, totalcount)
    print('------------------------------------------------------ total count : {} '.format(totalcount))
    image_path = os.path.join(file_path, file_string)
    #image.save(image_path, 'JPEG')
    cv2.imwrite(image_path, img)

    totalcount += 1

    if totalcount == 30:
        exit(0)


    return totalcount


def main():
    totalcount = 0
    for font in fonts:
        fontname = font
        for words in labels:
            bBigFont = False
            # origin words
            totalcount = saveWordsImage(words, fontname, totalcount)

            # Cappitalize words
            # words = words.capitalize()

            for bigfont in bigfontonly:
                if fontname[:-4] == bigfont:
                    bBigFont = True
                    break

            if bBigFont == False:
                # upper words
                words = words.upper()
                totalcount = saveWordsImage(words, fontname, totalcount)


if __name__ == '__main__':
    main()


