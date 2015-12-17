#! /bin/python3

import bmp


# TODO: switch to a different image manipulation format?


def lsb_basic(pixels, message, bits_used=1, password=None):
    # TODO: add encryption support
    bmp.check_pixels(pixels)
    result = bmp.copy(pixels)

    bits = _str_to_bits(message)
    bit_index = 0
    pixel_size = len(pixels[0][0])
    for row in pixels:
        for col_index in range(len(pixels)):
            row[col_index] = _process_pixel(row[col_index], bits, bit_index)
            bit_index += pixel_size
            if bit_index >= len(bits):
                return result
    raise ValueError('Message does not fit in the given bitmap')


def _process_pixel(pixel, msg_bits, index):
    result = []
    for band in pixel:
        if msg_bits[index]:
            value = band | 1
        else :
            value = band & 0xfe
        result.append(value)
        index += 1
    return tuple(result)


def _str_to_bits(string):
    result = []
    str_bytes = string.encode()
    for byte in str_bytes:
        bin_byte = bin(byte)[2:]
        result.extend([0]*(8 - len(bin_byte)))
        result.extend(int(bit) for bit in bin_byte)
    return result