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


def get_white_bg(bg_height: int, bg_width: int) -> cv.Mat:
    result = np.ones(shape=(bg_height, bg_width, 3), dtype=np.uint8)
    result *= np.iinfo(result.dtype).max
    return result


def get_spacing(bg_size: int, cards_size: int, cards_padding: int):
    n_cards = bg_size // (cards_size + cards_padding)
    spacing = (bg_size - n_cards * cards_size) / (n_cards + 1)  # float
    return spacing
    

def get_cut_bg(bg_height: int, bg_width: int, cards_height: int, cards_width: int, cut_thickness: int = 1, cut_color: tuple[3] = (0, 0, 0), frame: bool = True, cards_padding: int = 0) -> cv.Mat:
    result = get_white_bg(bg_height, bg_width)

    height_spacing = get_spacing(bg_height, cards_height, cards_padding)
    width_spacing = get_spacing(bg_width, cards_width, cards_padding)

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

    if frame:
        cv.line(img=result, pt1=(0, int(round(height_spacing / 2))), pt2=(bg_width-1, int(round(height_spacing / 2))), color=cut_color, thickness=cut_thickness)
        cv.line(img=result, pt1=(0, bg_height - int(round(height_spacing / 2))), pt2=(bg_width-1, bg_height - int(round(height_spacing / 2))), color=cut_color, thickness=cut_thickness)
        cv.line(img=result, pt1=(int(round(width_spacing / 2)), 0), pt2=(int(round(width_spacing / 2)), bg_height - 1), color=cut_color, thickness=cut_thickness)
        cv.line(img=result, pt1=(bg_width - int(round(width_spacing / 2)), 0), pt2=(bg_width - int(round(width_spacing / 2)), bg_height - 1), color=cut_color, thickness=cut_thickness)


    return result


# def get_white_bg_mm(height_mm: float, width_mm: float, dpi: int = 300) -> cv.Mat:
#     h_pixel = int(round((height_mm * dpi) / 25.4))
#     w_pixel = int(round((width_mm * dpi) / 25.4))

#     return get_white_bg(h_pixel, w_pixel)


# def get_cut_bg_mm(height_mm: float, width_mm: float, ch_mm: float, cw_mm: float, cut_thickness: int = 1, cut_color: tuple[3] = (0, 0, 0), dpi: int = 300, frame: bool = True, cards_padding: float = 0) -> cv.Mat:
#     h_pixel = int(round((height_mm * dpi) / 25.4))
#     w_pixel = int(round((width_mm * dpi) / 25.4))

#     ch_pixel = int(round((ch_mm * dpi) / 25.4))
#     cw_pixel = int(round((cw_mm * dpi) / 25.4))

#     cp_pixel = int(round(cards_padding * dpi) / 25.4)

#     return get_cut_bg(h_pixel, w_pixel, ch_pixel, cw_pixel, cut_thickness, cut_color, frame, cp_pixel)


# def get_white_bg_format(format: str, dpi: int = 300) -> cv.Mat:
#     if format not in print_formats:
#         raise Exception('Unknown format!')
    
#     h_mm, w_mm = print_formats[format]
#     return get_white_bg_mm(h_mm, w_mm, dpi)


# def get_cut_bg_format(format: str, cards_height: float, cards_width: float, cards_um: str, cut_thickness: int = 1, cut_color: tuple[3] = (0, 0, 0), dpi: int = 300, frame: bool = True, cards_padding: float = 0) -> cv.Mat:
#     if format not in print_formats:
#         raise Exception('Unknown format!')
    
#     if cards_um not in ['mm', 'inch']:
#         raise Exception('cards unit of measurement not valid, must be in [mm, inch]')
    
#     h_mm, w_mm = print_formats[format]
#     if cards_um == 'mm':
#         return get_cut_bg_mm(h_mm, w_mm, cards_height, cards_width, cut_thickness, cut_color, dpi, frame, cards_padding)
#     elif cards_um == 'inch':
#         h_inch = h_mm / 25.4
#         w_inch = w_mm / 25.4
#         return get_cut_bg_inches(h_inch, w_inch, cards_height, cards_width, cut_thickness, cut_color, dpi, frame, cards_padding)


# def get_white_bg_inches(height_inch: float, widht_inch: float, dpi: int = 300) -> cv.Mat:
#     h_pixel = int(round(height_inch * dpi))
#     w_pixel = int(round(widht_inch * dpi))

#     return get_white_bg(h_pixel, w_pixel)
    

# def get_cut_bg_inches(height_inch: float, widht_inch: float, cards_height: float, cards_width: float, cut_thickness: int = 1, cut_color: tuple[3] = (0, 0, 0), dpi: int = 300, frame: bool = True, cards_padding: float = 0) -> cv.Mat:
#     h_pixel = int(round(height_inch * dpi))
#     w_pixel = int(round(widht_inch * dpi))

#     ch_pixel = int(round(cards_height * dpi))
#     cw_pixel = int(round(cards_width * dpi))

#     cp_pixel = int(round(cards_padding * dpi))

#     return get_cut_bg(h_pixel, w_pixel, ch_pixel, cw_pixel, cut_thickness, cut_color, frame, cp_pixel)
    


if __name__ == '__main__':
    backgrounds = []
    backgrounds.append(get_cut_bg(1000, 500, 220, 140, frame=True))
    backgrounds.append(get_white_bg(300, 200))

    # backgrounds.append(get_white_bg_format('A3', 300))
    # backgrounds.append(get_white_bg_format('A3', 150))
    # backgrounds.append(get_white_bg_format('A4', 300))
    # backgrounds.append(get_white_bg_inches(11.7, 8.3, 300))
    # backgrounds.append(get_white_bg_mm(297, 210, 300))

    # backgrounds.append(get_cut_bg_format('A3', 89, 57.5, 'mm'))
    # backgrounds.append(get_cut_bg_format('A3', 88, 64, 'mm', dpi=150))
    # backgrounds.append(get_cut_bg_format('A4', 88, 63.5, 'mm'))
    # backgrounds.append(get_cut_bg_format('A4', 3.2, 2.2, 'inch'))
    # backgrounds.append(get_cut_bg_inches(11.7, 8.3, 3.2, 2.2))
    # backgrounds.append(get_cut_bg_mm(297, 210, 88, 63.5))
    # backgrounds.append(get_cut_bg_mm(440, 310, 88, 63.5))

    for i in range(len(backgrounds)):
        # cv.imshow(f'test-{i}', backgrounds[i])
        cv.imwrite(f'test-{i}.png', backgrounds[i])
    cv.waitKey(0)
    
    


    
    