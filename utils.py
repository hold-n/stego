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