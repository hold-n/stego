#! /bin/python

import bmp
import stego

import pdb


def main():
    _lsb_basic_read()


def _lsb_basic_read():
    bitmap = bmp.load('data/stego.bmp')
    print stego.extract_lsb_message_basic(bitmap)


def _lsb_basic_write():
    bitmap = bmp.load('data/bitmap.bmp')
    modified = stego.insert_lsb_message_basic(bitmap, 'hello world')
    bmp.save(modified, bmp.grayscale_palette(), 'data/stego.bmp')


def _make_grayscale():
    pixels = _get_stub_data(448, 256)
    bitmap = bmp.Bitmap(pixels)
    bmp.save(bitmap, bmp.grayscale_palette(), 'data/bitmap.bmp')


def _get_stub_data(width, height):
    return [
        [int(float(y)/height*256) for x in range(width)]
            for y in range(height)
        ]


if __name__ == '__main__':
    main()