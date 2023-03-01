

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

def mm_to_pixel(mm: float, dpi: int) -> int:
    return int(round((mm * dpi) / 25.4))


def inch_to_pixel(inch: float, dpi: int) -> int:
    return int(round(inch * dpi))


def get_sizes_from_mm(bg_h_mm: float, bg_w_mm: float, c_h_mm: float, c_w_mm: float, dpi: int) -> tuple:
    bg_h = mm_to_pixel(bg_h_mm, dpi)
    bg_w = mm_to_pixel(bg_w_mm, dpi)
    c_h = mm_to_pixel(c_h_mm, dpi)
    c_w = mm_to_pixel(c_w_mm, dpi)
    return bg_h, bg_w, c_h, c_w



def get_sizes_from_inch(bg_h_inch: float, bg_w_inch: float, c_h_inch: float, c_w_inch: float, dpi: int) -> tuple:
    bg_h = mm_to_pixel(bg_h_inch, dpi)
    bg_w = mm_to_pixel(bg_w_inch, dpi)
    c_h = mm_to_pixel(c_h_inch, dpi)
    c_w = mm_to_pixel(c_w_inch, dpi)
    return bg_h, bg_w, c_h, c_w


def get_size_from_format(format: str, c_h: float, c_w: float, dpi: int, cards_um: str) -> tuple:
    if format not in print_formats:
        raise Exception('Unknown format!')
    
    if cards_um not in ['mm', 'inch']:
        raise Exception('cards unit of measurement not valid, must be in [mm, inch]')
    
    h_mm, w_mm = print_formats[format]
    if cards_um == 'mm':
        return get_sizes_from_mm(h_mm, w_mm, c_h, c_w, dpi)
    elif cards_um == 'inch':
        h_inch = h_mm / 25.4
        w_inch = w_mm / 25.4
        return get_sizes_from_inch(h_inch, w_inch, c_h, c_w, dpi)