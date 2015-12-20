from Crypto.Hash import SHA256 as sha
from Crypto.Cipher import AES as aes


# can be any valid aes key size: 16, 24, 32
_AES_KEY_SIZE = 16


def bits_to_str(bits):
    result = bytearray()
    for byte_num in range(len(bits)/8):
        byte_digits = bits[byte_num*8:(byte_num+1)*8]
        result.append(int(''.join(str(b) for b in byte_digits), 2))
    return str(result)


def bytes_to_number(byte_array):
        '''
        Converts an iterable of bytes to integer.
        Implies little-endian byte order
        '''
        result = 0
        for byte in reversed(bytearray(byte_array)):
            result <<= 8
            result += byte
        return result


def decrypt_message(msg, password):
    if len(msg) % 16 != 0:
        raise ValueError(
            "Message size is not a multiple of a cipher block size. Maybe the message was not encrypted?"
        )
    processed_password = _process_password(password)
    cipher = aes.new(processed_password)
    return _strip_padding(cipher.decrypt(msg))


def encrypt_message(msg, password):
    processed_password = _process_password(password)
    cipher = aes.new(processed_password)
    return cipher.encrypt(_pad_message(msg))


def number_to_bytes(i, bytes_num=4):
    result = bytearray()
    for _ in range(bytes_num):
        result.append(i & 0xff)
        i >>= 8
    return str(result)


def str_to_bits(string):
    result = []
    for byte in string:
        bin_byte = bin(ord(byte))[2:]
        result.extend([0]*(8 - len(bin_byte)))
        result.extend(int(bit) for bit in bin_byte)
    return result


def _pad_message(msg):
    msg += b'1'
    # aes message size must be a multiple of 16
    msg += b'0'*(16 - (len(msg) % 16))
    return msg


def _process_password(password):
    hasher = sha.new()
    hasher.update(password)
    return hasher.digest()[:_AES_KEY_SIZE]


def _strip_padding(msg):
    zero_index = -1
    while msg[zero_index] == '0':
        zero_index -= 1
    return msg[:zero_index]
