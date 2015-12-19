from Crypto.Hash import SHA256 as sha
from Crypto.Cipher import AES as aes

import bmp
from utils import number_to_bytes, bytes_to_number, str_to_bits, bits_to_str

import pdb


# can be any valid aes key size: 16, 24, 32
_AES_KEY_SIZE = 16
# in bits, must be a multiple of 8
_SIZE_MARK_SIZE = 24

_SET_MASKS = {
    0: 1,
    1: 2,
    2: 4,
    3: 8,
    4: 16,
    5: 32,
    6: 64,
    7: 128,
}
_CLEAR_MASKS = {
    0: 0xfe,
    1: 0xfd,
    2: 0xfb,
    3: 0xf7,
    4: 0xef,
    5: 0xdf,
    6: 0xbf,
    7: 0x7f,
}


def extract_lsb_message_basic(bitmap, bits_used=1, password=None):
    if not 1 <= bits_used <= 8:
        raise ValueError('bits_used must be between 1 and 8')
    size = _get_size_mark(bitmap, bits_used)
    bits = []
    # TODO: consider the case when there's not enough space on one row for mark
    row_index = 0 # <-
    bit = _SIZE_MARK_SIZE % bits_used
    col_index = _SIZE_MARK_SIZE/bits_used
    row_length = bitmap.width*bitmap.bits_per_pixel/8
    # entangled loop flat loop so that it would be easier to break out
    while len(bits) < size*8:
        bits.append(1 if bitmap.pixels[row_index][col_index] & _SET_MASKS[bit] else 0
        )
        if bits_used - bit > 1:
            bit += 1
            continue
        else:
            bit = 0
        col_index += 1
        if col_index >= row_length:
            col_index = 0
            row_index += 1
            if row_index >= bitmap.height:
                raise ValueError("The specified message size is incorrect")
    message = bits_to_str(bits)
    if password is not None:
        message = _decrypt_message(message, password)
    return message


def insert_lsb_message_basic(bitmap, message, bits_used=1, password=None):
    if not 1 <= bits_used <= 8:
        raise ValueError('bits_used must be between 1 and 8')
    result = bitmap.copy()
    if password is not None:
        message = _encrypt_message(message, password)
    message = _add_size_mark(message)
    bits = str_to_bits(message)
    bit_index = 0
    row_len = len(bitmap.pixels[0])
    for row in result.pixels:
        for col_index in range(row_len):
            for bit in range(bits_used):
                if bits[bit_index]:
                    row[col_index] |= _SET_MASKS[bit]
                else:
                    row[col_index] &= _CLEAR_MASKS[bit]
                bit_index += 1
                if bit_index >= len(bits):
                    return result
    raise ValueError('Message does not fit in the given bitmap')


def _add_size_mark(msg):
    return number_to_bytes(len(msg), _SIZE_MARK_SIZE/8) + msg


def _decrypt_message(msg, password):
    if len(msg) % 16 != 0:
        raise ValueError("Message size is not a multiple of a cipher block size. Maybe the message was not encrypted?")
    processed_password = _process_password(password)
    cipher = aes.new(processed_password)
    return _strip_padding(cipher.decrypt(msg))


def _encrypt_message(msg, password):
    processed_password = _process_password(password)
    cipher = aes.new(processed_password)
    return cipher.encrypt(_pad_message(msg))


def _get_size_mark(bitmap, bits_used):
    bits = []
    bit_count = 0
    for row in bitmap.pixels:
        for byte in row:
            for bit in range(bits_used):
                bits.append(1 if (byte & _SET_MASKS[bit]) else 0)
                bit_count += 1
                if bit_count >= _SIZE_MARK_SIZE:
                    return bytes_to_number(bits_to_str(bits))


def _pad_message(msg):
    msg += b'1'
    # aes message size must be a multiple of 16
    msg += b'0'*(16 - (len(msg) % 16))
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


def _strip_padding(msg):
    zero_index = -1
    while msg[zero_index] == '0':
        zero_index -= 1
    return msg[:zero_index]
