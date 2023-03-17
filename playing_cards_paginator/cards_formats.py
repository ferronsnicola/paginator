
def get_h_w_mm_from_format(format: str):
    if format == 'Magic-Pokemon':
        return (88, 63.5)
    elif format == 'Yu-gi-oh!':
        return (86, 59)  # to check
    elif format == '7 Wonders':
        return (100, 65)
    elif format == '57.5x89':
        return (89, 57.5)
    elif format == '56x87':
        return (87, 56)
    else:
        raise Exception(f'format not known yet: {format}')
    
