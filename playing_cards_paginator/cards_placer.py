import cv2 as cv
import numpy as np
import background_generator as bgg
from os import listdir
from os.path import isfile, join, isdir


def get_files(bg_height: int, bg_width: int, c_height: int, c_width: int, fronts: list[cv.Mat], backs: list[cv.Mat], pad: int, frame: bool = True, cut_thickness: int = 1, cut_color: tuple = (0, 0, 0)) -> cv.Mat:
    result_front = []
    result_back = []

    background = bgg.get_cut_bg(bg_height, bg_width, c_height, c_width, cut_thickness, cut_color, frame, pad)
    vertical_spacing = bgg.get_spacing(bg_height, c_height, pad)
    horizontal_spacing = bgg.get_spacing(bg_width, c_width, pad)
    
    count = 0
    while len(fronts) > 0:
        x = horizontal_spacing
        y = vertical_spacing

        background_fronts = background.copy()
        background_backs = background.copy()

        while x <= bg_width - c_width - horizontal_spacing:
            card = None
            while y <= bg_height - c_height - vertical_spacing:
                if len(fronts) == 0:
                    break
                card = fronts.pop(0)
                back = backs.pop(0)

                xx = int(round(x)) - pad
                yy = int(round(y)) - pad

                card_pad = cv.copyMakeBorder(card, pad, pad, pad, pad, cv.BORDER_REPLICATE)
                back_pad = cv.copyMakeBorder(back, pad, pad, pad, pad, cv.BORDER_REPLICATE)

                background_fronts[yy : yy + c_height + 2 * pad, xx : xx + c_width + 2 * pad] = card_pad
                background_backs[yy : yy + c_height + 2 * pad, bg_width - xx - (c_width + 2 * pad) : bg_width - xx] = back_pad
                y += c_height + vertical_spacing

            if len(fronts) == 0:
                break

            x += c_width + horizontal_spacing
            y = vertical_spacing

        count += 1
        print(count)
        result_back.append(background_backs)
        result_front.append(background_fronts)

    return result_front, result_back

if __name__ == '__main__':
    fronts = []
    backs = []

    bg_width = 5200
    bg_height = 3660

    c_height = 1039
    c_width = 744

    cards_padding = 30

    app_dir = 'playing_cards_paginator'


    fronts_dirs = [dir for dir in listdir(join(app_dir, 'fronts')) if isdir(join(app_dir, 'fronts', dir))]
    backs_dirs = [dir for dir in listdir(join(app_dir, 'backs')) if isdir(join(app_dir, 'backs', dir))]

    if len(fronts_dirs) != len(backs_dirs):
        raise Exception(f'different number of backs and fronts source directories: fronts={len(fronts_dirs)}, backs={len(backs_dirs)}')
    for i in range(len(fronts_dirs)):
        if fronts_dirs[i] != backs_dirs[i]:
            raise Exception(f'fronts and backs directories must have the same names in order to match correctly!')
        
    
    for dir in fronts_dirs:
        front_names = [card_name for card_name in listdir(join(app_dir, 'fronts', dir)) if isfile(join(app_dir, 'fronts', dir, card_name))]
        back_name = [card_name for card_name in listdir(join(app_dir, 'backs', dir)) if isfile(join(app_dir, 'backs', dir, card_name))][0]
        back = cv.imread(join(app_dir, 'backs', dir, back_name), cv.IMREAD_COLOR)
        back = cv.resize(back, (c_width, c_height))

        for front_name in front_names:
            front = cv.imread(join(app_dir, 'fronts', dir, front_name), cv.IMREAD_COLOR)

            front = cv.resize(front, (c_width, c_height))

            fronts.append(front)
            backs.append(back)
    
    fronts, backs = get_files(bg_height, bg_width, c_height, c_width, fronts, backs, cards_padding)

    for i in range(len(fronts)):
        cv.imwrite(f'front-{i}.png', fronts[i])
        cv.imwrite(f'back-{i}.png', backs[i])





