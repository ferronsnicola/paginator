import cv2 as cv
import background_generator as bgg
from os import listdir
from os.path import isfile, join, isdir
import um_conversions as umc



def get_files_from_mm(bg_height_mm: float, bg_width_mm: float, c_height_mm: float, c_width_mm: float, fronts: list[cv.Mat], backs: list[cv.Mat], pad_mm: float, frame: bool = True, cut_thickness: int = 1, cut_color: tuple = (0, 0, 0), dpi: int = 300) -> cv.Mat:
    bg_height, bg_width, c_height, c_width = umc.get_sizes_from_mm(bg_height_mm, bg_width_mm, c_height_mm, c_width_mm, dpi)
    pad = umc.mm_to_pixel(pad_mm, dpi)
    return get_files(bg_height, bg_width, c_height, c_width, fronts, backs, pad, frame, cut_thickness, cut_color)


def get_files_from_inch(bg_height_inch: float, bg_width_inch: float, c_height_inch: float, c_width_inch: float, fronts: list[cv.Mat], backs: list[cv.Mat], pad_inch: float, frame: bool = True, cut_thickness: int = 1, cut_color: tuple = (0, 0, 0), dpi: int = 300) -> cv.Mat:
    bg_height, bg_width, c_height, c_width = umc.get_sizes_from_inch(bg_height_inch, bg_width_inch, c_height_inch, c_width_inch, dpi)
    pad = umc.inch_to_pixel(pad_inch, dpi)
    return get_files(bg_height, bg_width, c_height, c_width, fronts, backs, pad, frame, cut_thickness, cut_color)


def get_files_from_format(format: str, c_height: int, c_width: int, fronts: list[cv.Mat], backs: list[cv.Mat], pad: float, frame: bool = True, cut_thickness: int = 1, cut_color: tuple = (0, 0, 0), dpi: int = 300, cards_um: str = 'mm') -> cv.Mat:
    bg_height, bg_width, c_height, c_width = umc.get_size_from_format(format, c_height, c_width, dpi, cards_um)
    if cards_um == 'mm':
        pad = umc.mm_to_pixel(pad, dpi)
    elif cards_um == 'inch':
        pad = umc.inch_to_pixel(pad, dpi)
    else:
        raise Exception('cards unit of measurement must be in [mm, inch]!')
    
    return get_files(bg_height, bg_width, c_height, c_width, fronts, backs, pad, frame, cut_thickness, cut_color)
    




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
                card = cv.resize(card, (c_width, c_height))

                back = backs.pop(0)
                back = cv.resize(back, (c_width, c_height))

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

    c_height = 87
    c_width = 56

    cards_padding = 2

    app_dir = 'playing_cards_paginator'

    format = 'A4'

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

        for front_name in front_names:
            front = cv.imread(join(app_dir, 'fronts', dir, front_name), cv.IMREAD_COLOR)

            fronts.append(front)
            backs.append(back)
    
    # fronts, backs = get_files(bg_height, bg_width, c_height, c_width, fronts, backs, cards_padding)
    fronts, backs = get_files_from_format(format, c_height, c_width, fronts, backs, cards_padding)

    for i in range(len(fronts)):
        cv.imwrite(f'front-{i}.png', fronts[i])
        cv.imwrite(f'back-{i}.png', backs[i])





