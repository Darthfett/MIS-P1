# 3rd party imports
from wand.image import Image

# built-in libraries
import os
import sys

# project libraries
pass

def main(args):
    # Should open the fail.png file and print its resolution (1920 x 1080).
    with Image(filename='fail.png') as img:
        print 'width:', img.width, 'height:', img.height

main(sys.argv[1:]) # skip first argument ("main.py")