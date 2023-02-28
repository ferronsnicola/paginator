import cv2 as cv
import numpy as np

print_formats = {
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


def get_white_bg_mm(height_mm: float, width_mm: float, dpi: int = 300):
    h_pixel = int(round((height_mm * dpi) / 25.4))
    w_pixel = int(round((width_mm * dpi) / 25.4))

    return get_white_bg(h_pixel, w_pixel)


def get_white_bg_format(format: str, dpi: int = 300):
    if format not in print_formats:
        raise Exception('Unknown format!')
    
    h_mm, w_mm = print_formats['format']
    return get_white_bg_mm(h_mm, w_mm, dpi)


def get_white_bg_inches(height_inch: float, widht_inch: float, dpi: int = 300):
    h_pixel = int(round(height_inch / dpi))
    w_pixel = int(round(widht_inch / dpi))

    return get_white_bg(h_pixel, w_pixel)
    


if __name__ == '__main__':
    bg = get_bg_with_cut_lines(1000, 500, 220, 140)

    cv.imshow('test', bg)
    cv.waitKey(0)
    
    


    
    