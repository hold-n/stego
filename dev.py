#! /bin/python

import bmp
import lsb

import pdb


MESSAGE = '''Han Solo is a fictional character in the Star Wars franchise, portrayed in films by Harrison Ford. In the original film trilogy, Han and his co-pilot, Chewbacca, become involved in the Rebel Alliance which opposes the Galactic Empire. During the course of the Star Wars story, he becomes a chief figure in the Alliance and succeeding galactic governments. Star Wars creator George Lucas described the character as "a loner who realizes the importance of being part of a group and helping for the common good".[1]
On Tatooine, Solo accepts a charter to transport Luke Skywalker, Ben Kenobi, C-3PO and R2-D2 to Alderaan in his Millennium Falcon spaceship for a payment which will help him clear debt. But when the crew and passengers arrive at the planet's coordinates, they discover that Alderaan has been destroyed by the Death Star. The Falcon is then captured and held within the battle station, however Han Solo, Chewbacca and his passengers evade capture by hiding in the ship smuggling compartments. While trying to find a way to escape, they discover that Princess Leia Organa is being held captive aboard the station. Enticed by the likelihood of a large reward, Solo and Chewbacca help Skywalker rescue the princess and escape from the Death Star
After delivering Skywalker, Leia and the droids to the Rebel Alliance, Solo and his Wookiee co-pilot receive payment for their services. Unfortunately the Millennium Falcon has been tracked to the Rebel Alliance moon base by the Death Star. The rebels plan to attack the space station and exploit a weakness in the space station's defences. Solo initially does not want to get involved in the planned attack because of his debt. Solo leaves with his reward and the rebels attack the Death Star. However, Solo has a change of heart and returns to save Luke's life during the film's climactic battle scene, ultimately enabling Luke to destroy the Death Star. For his heroics, Solo is presented with a medal of honour.
'''

SMALL_MSG = 'hello'

PASSWORD = 'password'

INFILE = 'data/Lenna.bmp'
MY_BITMAP = 'data/bitmap.bmp'
OUTFILE = 'data/stego.bmp'


def main():
    _lsb_write()


def _lsb_read():
    bitmap = bmp.load(OUTFILE)
    print lsb.extract(
        bitmap, PASSWORD, bits_used=5
    )


def _lsb_write():
    bitmap = bmp.load(INFILE)
    modified = lsb.insert(
        bitmap, PASSWORD, MESSAGE, bits_used=1
    )
    bmp.save(modified, bmp.rgb_palette(), OUTFILE)


def _make_grayscale():
    pixels = _get_stub_data(448, 256)
    bitmap = bmp.Bitmap(pixels)
    bmp.save(bitmap, bmp.grayscale_palette(), MY_BITMAP)


def _get_stub_data(width, height):
    return [
        [int(float(y)/height*256) for x in range(width)]
            for y in range(height)
        ]


if __name__ == '__main__':
    main()
