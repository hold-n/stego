import bmp


# TODO: switch to a different image manipulation format


def lsb_basic(pixels, message, bits_used=1, password=None):
    # TODO: add encryption support
    message_bytes = message.encode()
