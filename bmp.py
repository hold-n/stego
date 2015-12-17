#! /bin/python3

import PIL.Image as image


def check_pixels(pixels):
    width = len(pixels[0])
    if not all(len(row) == width for row in pixels):
        raise ValueError("Width has to be the same for all rows")
    pixel_size = len(pixels[0][0])
    for row in pixels:
        for pixel in row:
            if len(pixel) != pixel_size:
                raise ValueError('Pixel size must be consistent')


def copy(pixels):
    return [row[:] for row in pixels]


def grayscale_bitmap(pixels):
    return _bitmap(
        pixels,
        _grayscale_dib_header,
        _grayscale_linear_palette()
    )


def load_bitmap(filename):
    bitmap = image.open(filename)
    pixels = list(bitmap.getdata())
    width = bitmap.width
    return [
        pixels[(r*width):((r+1)*width)]
        for r in range(bitmap.height)
    ]


def rgb_bitmap(pixels):
    check_pixels(pixels)
    height = len(pixels)
    width = len(pixels[0])

    bitmap = bytearray()
    bitmap.extend(_bmp_header_with_stubs())
    bitmap.extend(_rgd_dib_header(width, height))


def _bitmap(pixels, dib_header_getter, palette):
    check_pixels(pixels)
    height = len(pixels)
    width = len(pixels[0])

    bitmap = bytearray()
    bitmap.extend(_bmp_header_with_stubs())
    bitmap.extend(dib_header_getter(width, height))
    bitmap.extend(palette)
    pixel_array_offset = len(bitmap)
    # bmps are bottom to top
    for row in reversed(pixels):
        for pixel in row:
            bitmap.extend(pixel)
    _update_bmp_header(bitmap, pixel_array_offset)
    return bitmap


def _get_stub_data(width, height):
    return [
        [(int(y/height*256),) for x in range(width)]
            for y in range(height)
        ]


def _bmp_header_with_stubs():
    header = bytearray()
    header.extend(b'BM')
    header.extend(b'\x00\x00\x00\x00') # placeholder for file size
    header.extend(b'\x00\x05') # reserved - zero
    header.extend(b'\x00\x00') # reserved - zero
    header.extend(b'\x00\x00\x00\x00') # placeholder for pixel array offset
    return header


def _grayscale_dib_header(width, height):
    header = bytearray()
    header.extend(b'\x28\x00\x00\x00') # image header size
    header.extend(_int32_to_bytes(width))
    header.extend(_int32_to_bytes(height))
    header.extend(b'\x01\x00') # number of image planes
    header.extend(b'\x08\x00') # bits per pixel
    header.extend(b'\x00\x00\x00\x00') # no compression
    header.extend(b'\x00\x00\x00\x00') # zero for uncompressed images
    header.extend(b'\x00\x00\x00\x00') # unused pixels per meter
    header.extend(b'\x00\x00\x00\x00') # unused pixels per meter
    header.extend(b'\x00\x00\x00\x00') # use whole color table
    header.extend(b'\x00\x00\x00\x00') # all colors are important
    return header


def _grayscale_linear_palette():
    result = []
    for c in range(0x100):
        result.extend([c, c, c, 0])
    return result


def _int32_to_bytes(i):
    return (
        i & 0xff,
        i >> 8 & 0xff,
        i >> 16 & 0xff,
        i >> 24 & 0xff
    )


def _read_bytearray(filename):
    with open(filename, 'rb') as f:
        return bytearray(f.read())


def _update_bmp_header(bitmap, pixel_array_offset):
    '''
    Updates placeholders in the bitmap after it has been fully constructed
    '''
    bitmap[2:6] = _int32_to_bytes(len(bitmap))
    bitmap[10:14] = _int32_to_bytes(pixel_array_offset)


def _write_bytearray(array, filename):
    with open(filename, 'wb') as f:
        f.write(array)
