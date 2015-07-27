#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
import sys
import os

from tiles import ImageTiles

DEFAULT_TILE_FOLDER = 'image_tiling_server/data/tiles'

def main():
  parser = optparse.OptionParser(usage='Usage: %prog [options] image_filename')

  parser.add_option('-d', '--destionation', dest='dest',
    default=DEFAULT_TILE_FOLDER,
    help='Location of image tiles. Default: <project_dir>/data/tiles')
  
  parser.add_option('-s', '--tile_size', dest='tile_size', type='int',
    default=64, help='Pixel size of the tiles. Default:')

  parser.add_option('-f', '--tile_format', dest='tile_format',
    default='jpg', help='Image format of the tiles. Default: jpg')

  (options, args) = parser.parse_args()

  if not args:
    parser.print_help()
    sys.exit(1)

  src_filename = args[0]

  tiles = ImageTiles(src_filename, options.tile_size, options.tile_format)
  
  parent_dir = os.path.join(os.path.dirname(__file__), os.pardir)
  tiles.create_tiles(os.path.join(parent_dir, options.dest))

if __name__ == '__main__':
  main()