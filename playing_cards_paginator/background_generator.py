import cv2 as cv
import numpy as np


def get_white_bg(bg_height: int, bg_width: int):
    result = np.ones(shape=(bg_height, bg_width, 3), dtype=np.uint8)
    result *= np.iinfo(result.dtype).max
    return result
    

def get_bg_with_cut_lines(bg_height: int, bg_width: int, cards_height: int, cards_width: int, cut_thickness: int = 1, cut_color: tuple[3] = (0, 0, 0)):
    result = get_white_bg(bg_height, bg_width)
    
    n_vertical_cards = bg_height // cards_height
    n_horizontal_cards = bg_width // cards_width

    height_spacing = (bg_height - n_vertical_cards * cards_height) / (n_vertical_cards + 1)  # float
    width_spacing = (bg_width - n_horizontal_cards * cards_width) / (n_horizontal_cards + 1)  # float


    y = height_spacing
    while y <= bg_height:
        yy = int(round(y))
        cv.line(img=result, pt1=(0, yy), pt2=(bg_width-1, yy), color=cut_color, thickness=cut_thickness)

        h = int(round(height_spacing))
        cv.line(img=result, pt1=(0, yy - h), pt2=(bg_width-1, yy - h), color=cut_color, thickness=cut_thickness)

        y += cards_height + height_spacing
    
    x = width_spacing
    while x <= bg_width:
        xx = int(round(x))
        cv.line(img=result, pt1=(xx, 0), pt2=(xx, bg_height - 1), color=cut_color, thickness=cut_thickness)

        w = int(round(width_spacing))
        cv.line(img=result, pt1=(xx - w, 0), pt2=(xx - w, bg_height - 1), color=cut_color, thickness=cut_thickness)

        x += cards_width + width_spacing

    return result


if __name__ == '__main__':
    bg = get_bg_with_cut_lines(1000, 500, 220, 140)

    cv.imshow('test', bg)
    cv.waitKey(0)
    
    


    
    