#! /bin/python

from itertools import chain

from Crypto.Hash import SHA256 as sha
from Crypto.Cipher import AES as aes

import bmp
from utils import number_to_bytes, bytes_to_number, str_to_bits, bits_to_str

import pdb

# can be any valid aes key size: 16, 24, 32
_AES_KEY_SIZE = 16
# in bits, must be a multiple of 8
_SIZE_MARK_SIZE = 24


def extract_lsb_message_basic(bitmap, bits_used=1, password=None):
    # TODO: add support for variable bits_used
    size = _get_size_mark(bitmap, bits_used)
    bits = []

    # processing the first row differently because of the size mark
    for byte in bitmap.pixels[0][_SIZE_MARK_SIZE:]:
        bits.append(byte & 1)
        if len(bits) >= size*8:
            break
    row_index = 1
    col_index = 0
    row_length = bitmap.width*bitmap.bits_per_pixel
    while len(bits) < size*8:
        bits.append(bitmap.pixels[row_index][col_index] & 1)
        col_index += 1
        if col_index >= row_length:
            col_index = 0
            row_index += 1
            if row_index >= bitmap.height:
                break
    message = bits_to_str(bits)
    if password is not None:
        message = _decrypt_message(message, password)
    return message


def insert_lsb_message_basic(bitmap, message, bits_used=1, password=None):
    # TODO: add support for variable bits_used
    result = bitmap.copy()
    message = _add_size_mark(message)
    if password is not None:
        message = _encrypt_message(message, password)
    bits = str_to_bits(message)
    bit_index = 0
    row_len = len(bitmap.pixels[0])
    for row in result.pixels:
        for col_index in range(row_len):
            if bits[bit_index]:
                row[col_index] = row[col_index] | 1
            else:
                row[col_index] = row[col_index] & 0xfe
            bit_index += 1
            if bit_index >= len(bits):
                return result
    raise ValueError('Message does not fit in the given bitmap')


def _add_size_mark(msg):
    return number_to_bytes(len(msg), _SIZE_MARK_SIZE/8) + msg


def _decrypt_message(msg, password):
    processed_password = _process_password(password)
    cipher = aes.new()
    return _strip_padding(cipher.decrypt(msg))


def _encrypt_message(msg, password):
    processed_password = _process_password(password)
    cipher = aes.new()
    return cipher.encrypt(_pad_message(msg))


def _get_size_mark(bitmap, bits_used):
    # TODO: add support for variable bits_used
    bits = []
    bit_count = 0
    for row in bitmap.pixels:
        for byte in row:
            bits.append(byte & 1)
            bit_count += 1
            if bit_count >= _SIZE_MARK_SIZE:
                return bytes_to_number(bits_to_str(bits))


def _pad_message(msg):
    msg += b'1'
    # aes message size must be a multiple of 16
    msg += b'0'*(len(msg) % 16)
    return msg


def _process_password(password):
    hasher = sha.new()
    hasher.update(password)
    return hasher.digest()[:_AES_KEY_SIZE]


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


def _strip_padding(bits):
    zero_count = 1
    while msg[-zero_count] == 0:
        zero_count += 1
    return msg[:-zero_count]