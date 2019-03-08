def get_point(row, col, subrow=0, subcol=0):
    """Получение точки по row col"""
    return 64 * col + subrow * 32, 64 * row + subcol * 32


def get_subindex(_x, _y):
    """Получение индекса для подклетки"""
    row = _x % 64
    col = _y % 64

    if row == 0:
        if not col == 0:
            return "Image_03"
        else:
            return "Image_01"

    if col == 0:
        if not row == 0:
            return "Image_04"
        else:
            return "Image_02"


def intersects(rect1, rect2):
    clipped = rect1.clip(rect2)

    return clipped.width > 0 or clipped.height > 0
