import cv2 as cv
from . import background_generator as bgg
from os import listdir
from os.path import isfile, join, isdir
from . import um_conversions as umc
import os
import shutil
from PIL import Image

plotter_formats = {
    'junior-legal': (203, 127),
    'letter': (279, 216),
    'legal': (356, 216),
    'tabloid': (432, 279),
    'A4': (297, 210),
    'A3': (420, 297),
    'A2': (594, 420),
    'A1': (841, 594),
    'A0': (1189, 841)
}

cards_formats = {
    'Magic-Pokemon': (88, 63.5),
    'Yu-gi-oh!': (86, 59),  # to check
    '7 Wonders': (100, 65),
    '57.5x89': (89, 57.5),
    '56x87': (87, 56),
}

def get_output_file(base_dir: str, plotter_height: float, plotter_width: float, cards_height: float, cards_width: float, pad: int, cut_lines: bool, frame_lines: bool, um: str, overlay_cut_cross: bool = False):
    fronts = []
    backs = []
    fronts_dirs = [dir for dir in listdir(join(base_dir, 'fronts')) if isdir(join(base_dir, 'fronts', dir))]
    backs_dirs = [dir for dir in listdir(join(base_dir, 'backs')) if isdir(join(base_dir, 'backs', dir))]

    if len(fronts_dirs) != len(backs_dirs):
        raise Exception(f'different number of backs and fronts source directories: fronts={len(fronts_dirs)}, backs={len(backs_dirs)}')
    for i in range(len(fronts_dirs)):
        if fronts_dirs[i] != backs_dirs[i]:
            raise Exception(f'fronts and backs directories must have the same names in order to match correctly!')
        
    
    for dir in fronts_dirs:
        front_names = [card_name for card_name in listdir(join(base_dir, 'fronts', dir)) if isfile(join(base_dir, 'fronts', dir, card_name))]
        back_name = [card_name for card_name in listdir(join(base_dir,  'backs', dir)) if isfile(join(base_dir, 'backs', dir, card_name))][0]
        back = cv.imread(join(base_dir, 'backs', dir, back_name), cv.IMREAD_COLOR)
        if back is None:
            back_name = [card_name for card_name in listdir(join(base_dir,  'backs', dir)) if isfile(join(base_dir, 'backs', dir, card_name))][1]
            back = cv.imread(join(base_dir, 'backs', dir, back_name), cv.IMREAD_COLOR)

        if back.shape[1] > back.shape[0]:
            back = cv.rotate(back, cv.ROTATE_90_CLOCKWISE)

        for front_name in front_names:
            if not (front_name.endswith('.png') or front_name.endswith('.jpg') or front_name.endswith('.tif')):
                continue
            front = cv.imread(join(base_dir, 'fronts', dir, front_name), cv.IMREAD_COLOR)

            if front.shape[1] > front.shape[0]:
                front = cv.rotate(front, cv.ROTATE_90_CLOCKWISE)

            fronts.append(front)
            backs.append(back)

    fronts, backs = get_files_from_mm(plotter_height, plotter_width, cards_height, cards_width, fronts, backs, pad, frame_lines, cut_lines, overlay_cut_cross=overlay_cut_cross)
    if not os.path.exists(join(base_dir, 'output')):
        os.mkdir(join(base_dir, 'output'))

    for i in range(len(fronts)):
        cv.imwrite(join(base_dir, 'output', f'front-{i}.png'), fronts[i])
        cv.imwrite(join(base_dir, 'output', f'back-{i}.png'), backs[i])

    lfronts = len(fronts)
    del(fronts)
    del(backs)

    images = []
    for i in range(lfronts):
        images.append(Image.open(join(base_dir, 'output', f'front-{i}.png')).convert("RGB"))
        images.append(Image.open(join(base_dir, 'output', f'back-{i}.png')).convert("RGB"))
    images[0].save(join(base_dir, 'output.pdf'), resolution=300.0, save_all=True, append_images=images[1:], quality=95)
    
    # shutil.make_archive(join(base_dir, 'output'), 'zip', join(base_dir, 'output'))
    shutil.rmtree(join(base_dir, 'output'))
    return join(base_dir, 'output.pdf')


def get_files_from_mm(bg_height_mm: float, bg_width_mm: float, c_height_mm: float, c_width_mm: float, fronts: list[cv.Mat], backs: list[cv.Mat], pad_mm: float, frame: bool = True, cut_lines: bool = True, cut_thickness: int = 1, cut_color: tuple = (0, 0, 0), dpi: int = 300, min_space: int = 2, overlay_cut_cross: bool = False) -> cv.Mat:
    bg_height, bg_width, c_height, c_width = umc.get_sizes_from_mm(bg_height_mm, bg_width_mm, c_height_mm, c_width_mm, dpi)
    pad = umc.mm_to_pixel(pad_mm, dpi)
    return get_files(bg_height, bg_width, c_height, c_width, fronts, backs, pad, frame, cut_lines, cut_thickness, cut_color, umc.mm_to_pixel(min_space, dpi), overlay_cut_cross)


def get_files_from_inch(bg_height_inch: float, bg_width_inch: float, c_height_inch: float, c_width_inch: float, fronts: list[cv.Mat], backs: list[cv.Mat], pad_inch: float, frame: bool = True, cut_thickness: int = 1, cut_color: tuple = (0, 0, 0), dpi: int = 300, overlay_cut_cross: bool = False) -> cv.Mat:
    bg_height, bg_width, c_height, c_width = umc.get_sizes_from_inch(bg_height_inch, bg_width_inch, c_height_inch, c_width_inch, dpi)
    pad = umc.inch_to_pixel(pad_inch, dpi)
    return get_files(bg_height, bg_width, c_height, c_width, fronts, backs, pad, frame, cut_thickness, cut_color, overlay_cut_cross)


def get_files_from_format(format: str, c_height: int, c_width: int, fronts: list[cv.Mat], backs: list[cv.Mat], pad: float, frame: bool = True, cut_thickness: int = 1, cut_color: tuple = (0, 0, 0), dpi: int = 300, cards_um: str = 'mm', overlay_cut_cross: bool = False) -> cv.Mat:
    bg_height, bg_width, c_height, c_width = umc.get_size_from_format(format, c_height, c_width, dpi, cards_um)
    if cards_um == 'mm':
        pad = umc.mm_to_pixel(pad, dpi)
    elif cards_um == 'inch':
        pad = umc.inch_to_pixel(pad, dpi)
    else:
        raise Exception('cards unit of measurement must be in [mm, inch]!')
    
    return get_files(bg_height, bg_width, c_height, c_width, fronts, backs, pad, frame, cut_thickness, cut_color, overlay_cut_cross)


def get_corner_cross_color(corner_color: tuple) -> tuple:
    # avg = (corner_color[0] + corner_color[1] + corner_color[2]) // 3
    result = [0, 0, 0]
    # if avg > 64:
    #     result = corner_color // 1.2
    # else:
    #     result = corner_color * 1.2
    for i in range(len(result)):
        if corner_color[i] > 64:
            result[i] = corner_color[i] // 1.2
        else:
            result[i] = corner_color[i] * 1.9
    # print(f'{corner_color} - {result}')
    return result
    

def check_consistency(cards_size: int, pad: int, bg_size: int, min_space_between_pad: int = 2) -> bool:
    spacing = bgg.get_spacing(bg_size, cards_size, pad, min_space_between_pad)
    print(f'spacing: {spacing}, min_space: {min_space_between_pad}')
    return spacing - 2*pad > min_space_between_pad


def get_files(bg_height: int, bg_width: int, c_height: int, c_width: int, fronts: list[cv.Mat], backs: list[cv.Mat], pad: int, frame: bool = True, cut_lines: bool = True, cut_thickness: int = 1, cut_color: tuple = (0, 0, 0), min_space: int = 30, overlay_cut_cross: bool = False) -> cv.Mat:
    result_front = []
    result_back = []

    if cut_lines:
        background = bgg.get_cut_bg(bg_height, bg_width, c_height, c_width, cut_thickness, cut_color, frame, pad, min_space)
    else:
        background = bgg.get_white_bg(bg_height, bg_width)
    vertical_spacing = bgg.get_spacing(bg_height, c_height, pad, min_space)
    horizontal_spacing = bgg.get_spacing(bg_width, c_width, pad, min_space)
    
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

                print(f'Overlay: {overlay_cut_cross}')

                if overlay_cut_cross:
                    corner_up_left = get_corner_cross_color(back[0][0])
                    corner_up_right = get_corner_cross_color(back[0][-1])
                    corner_down_left = get_corner_cross_color(back[-1][0])
                    corner_down_right = get_corner_cross_color(back[-1][-1])
                    
                    back_pad = cv.line(back_pad, (2 * pad // 3, pad), (4 * pad // 3, pad), corner_up_left, 1)
                    back_pad = cv.line(back_pad, (pad, 2 * pad // 3), (pad, 4 * pad // 3), corner_up_left, 1)

                    back_pad = cv.line(back_pad, (2 * pad // 3, c_height + pad), (4 * pad // 3, c_height + pad), corner_down_left, 1)
                    back_pad = cv.line(back_pad, (pad, c_height + 2 * pad // 3), (pad, c_height + 4 * pad // 3), corner_down_left, 1)

                    back_pad = cv.line(back_pad, (c_width + 2 * pad // 3, pad), (c_width + 4 * pad // 3, pad), corner_up_right, 1)
                    back_pad = cv.line(back_pad, (c_width + pad, 2 * pad // 3), (c_width + pad, 4 * pad // 3), corner_up_right, 1)

                    back_pad = cv.line(back_pad, (c_width + 2 * pad // 3, c_height + pad), (c_width + 4 * pad // 3, c_height + pad), corner_down_right, 1)
                    back_pad = cv.line(back_pad, (c_width + pad, c_height + 2 * pad // 3), (c_width + pad, c_height + 4 * pad // 3), corner_down_right, 1)

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





