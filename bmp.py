from utils import bytes_to_number, number_to_bytes


_SIZE_OFFSET = 2
_SIZE_LEN = 4

_DATA_OFFSET = 10
_DATA_LEN = 4

_BITS_PER_PIXEL_OFFSET = 28
_BITS_PER_PIXEL_LEN = 2

_HEIGHT_OFFSET = 22
_WIDTH_OFFSET = 18
_DIM_LEN = 2


# TODO: add support for ICC Color pixelsrofile section


class Bitmap(object):
    '''
    Represents a bitmap. This class only incapsulates data,
    implementing data access behaviour and leaving all data manipulation
    such as bmp format parsing to external functions
    '''
    def __init__(self, pixels, bits_per_pixel=8):
        check_pixels(pixels)
        if round(bits_per_pixel/8) != bits_per_pixel/8:
            raise ValueError(
                "Number of bits per pixel must be a multiple of 8 for this implementation"
            )
        self.pixels = [bytearray(row) for row in pixels]
        self.height = len(pixels)
        self.width = len(pixels[0])/bits_per_pixel*8
        self.bits_per_pixel = bits_per_pixel

    def copy(self):
        return Bitmap(self.pixels, self.bits_per_pixel)

    def pixel(self, x, y):
        '''
        Returns the number representing the pixel at the position (x, y)
        Indeces are zero-based
        '''
        if x > self.width or y > self.height:
            raise ValueError('Coordinates outside of the bitmap size')
        self.pixels[y][x*band_num:(x+1)*band_num]

    def bit_size(self):
        return self.width * self.height * self.bits_per_pixel


def check_pixels(pixels):
        width = len(pixels[0])
        if not all(len(row) == width for row in pixels):
            raise ValueError("Width has to be the same for all rows")


def grayscale_palette():
    result = []
    for c in range(0x100):
        result.extend([c, c, c, 0])
    return result


def load(filename):
    with open(filename, 'rb') as f:
        data = bytearray(f.read())
    if not data.startswith('BM'):
        raise ValueError('Invalid data format')
    return _parse_bmp(data)


def rgb_palette():
    return []


def save(bitmap, palette, filename):
    with open(filename, 'wb') as f:
        f.write(_form_bmp(bitmap, palette))


def _bitmapinfoheader(width, height, bits_per_pixel=8):
    header = bytearray()
    header.extend(b'\x28\x00\x00\x00') # image header size
    header.extend(number_to_bytes(width))
    header.extend(number_to_bytes(height))
    header.extend(b'\x01\x00') # number of image planes
    header.extend(number_to_bytes(bits_per_pixel, 2)) # bits per pixel
    header.extend(b'\x00\x00\x00\x00') # no compression
    header.extend(b'\x00\x00\x00\x00') # zero for uncompressed images
    header.extend(b'\x00\x00\x00\x00') # unused pixels per meter
    header.extend(b'\x00\x00\x00\x00') # unused pixels per meter
    header.extend(b'\x00\x00\x00\x00') # use whole color table
    header.extend(b'\x00\x00\x00\x00') # all colors are important
    return header


def _file_header_stub():
    header = bytearray()
    header.extend(b'BM')
    header.extend(b'\x00\x00\x00\x00') # placeholder for file size
    header.extend(b'\x00\x00') # reserved - zero
    header.extend(b'\x00\x00') # reserved - zero
    header.extend(b'\x00\x00\x00\x00') # placeholder for pixel array offset
    return header


def _form_bmp(bitmap, palette):
    check_pixels(bitmap.pixels)
    data = bytearray()
    data.extend(_file_header_stub())
    data.extend(_bitmapinfoheader(
        bitmap.width, bitmap.height, bitmap.bits_per_pixel
    ))
    data.extend(palette)
    pixel_array_offset = len(data)
    # bmps are bottom to top
    for row in reversed(bitmap.pixels):
        data.extend(row)
    _update_bmp_header(data, pixel_array_offset)
    return data


def _grayscale_palette():
    result = []
    for c in range(0x100):
        result.extend([c, c, c, 0])
    return result


def _parse_bmp(data):
    pixel_array_offset = bytes_to_number(
        data[_DATA_OFFSET:_DATA_OFFSET+_DATA_LEN]
    )
    bits_per_pixel = bytes_to_number(
        data[_BITS_PER_PIXEL_OFFSET:_BITS_PER_PIXEL_OFFSET+_BITS_PER_PIXEL_LEN]
    )
    width = bytes_to_number(data[_WIDTH_OFFSET:_WIDTH_OFFSET+_DIM_LEN])
    height = bytes_to_number(data[_HEIGHT_OFFSET:_HEIGHT_OFFSET+_DIM_LEN])
    data = data[pixel_array_offset:]
    if height*width*bits_per_pixel/8 != len(data):
        raise ValueError('Invalid data format')
    row_size = width*bits_per_pixel/8
    return Bitmap(
        [data[(h*row_size):((h+1)*row_size)] for h in range(height-1, -1, -1)],
        bits_per_pixel
    )


def _update_bmp_header(data, pixel_array_offset):
    '''
    Updates placeholders in the bitmap after it has been fully constructed
    '''
    data[_SIZE_OFFSET:_SIZE_OFFSET+_SIZE_LEN] = number_to_bytes(len(data))
    data[_DATA_OFFSET:_DATA_OFFSET+_DATA_LEN] = number_to_bytes(
        pixel_array_offset
    )
