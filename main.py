#! /bin/python

import argparse

import lsb
import bmp


DEFAULT_PASSWORD = 'default_password'


def get_args():
    parser = argparse.ArgumentParser(description='A steganography tool for bitmaps')
    parser.add_argument('infile', help='Path to the file to process')
    parser.add_argument(
        '-e', '--extract', action='store_true',
        help='Extract message from the image. the default behaviour is writing a message'
    )
    parser.add_argument(
        '-p', '--password', help='The password used to encrypt the message'
    )
    parser.add_argument(
        '-m', '--message-file',
        help='The name of the file that contains the message to be inserted into the image'
    )
    parser.add_argument(
        '-b', '--bits-used', type=int,
        help='Number of bits in a byte to use for the algorithm'
    )
    parser.add_argument(
        '-o', '--outfile',
        help='If inserting a message, specifies the file to write the result to'
    )
    return parser.parse_args()


def lsb_read(filename, password, bits_used):
    bitmap = bmp.load(filename)
    print lsb.extract(
        bitmap, password, bits_used
    )


def lsb_write(in_filename, out_filename, password, message, bits_used):
    bitmap = bmp.load(in_filename)
    modified = lsb.insert(
        bitmap, password, message, bits_used
    )
    bmp.save(modified, bmp.rgb_palette(), out_filename)


def process_args(args):
    if not args.extract:
        if args.outfile is None:
            raise ValueError(
                'You must specify the output file upon inserting a message'
            )
        if args.message_file is None:
            raise ValueError(
                'You must specify the message file upon inserting'
            )
    password = args.password if args.password is not None else DEFAULT_PASSWORD
    bits_used = args.bits_used if args.bits_used else 1
    if args.extract:
        lsb_read(args.infile, password, bits_used)
    else:
        with open(args.message_file) as f:
            message = f.read()
        lsb_write(args.infile, args.outfile, password, message, bits_used)


if __name__ == '__main__':
    args = get_args()
    process_args(args)
