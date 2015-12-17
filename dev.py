#! /bin/python3

import bmp
import stego


def main():
    _lsb_basic()


def _lsb_basic():
    bitmap = bmp.load_bitmap('data/Pencil_icon1.bmp')
    modified = stego.lsb_basic(bitmap, 'hello world')
    print(modified)


def _make_grayscale():
    bitmap = bmp.grayscale_bitmap(bmp._get_stub_data(448, 256))
    bmp._write_bytearray(bitmap, 'data/bitmap.bmp')


if __name__ == '__main__':
    main()