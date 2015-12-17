import bmp


def main():
    bitmap = grayscale_bitmap(_get_stub_data(448, 256))
    _write_bytearray(bitmap, 'data/bitmap.bmp')


if __name__ == '__main__':
    main()