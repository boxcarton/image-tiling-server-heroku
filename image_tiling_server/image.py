#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import math
from PIL import Image

class ImageMaker(object):
  def __init__(self, level, x, y, width, height, tile_folder):
    self.level = level
    self.x = int(x)
    self.y = int(y)
    self.width = int(width)
    self.height = int(height)
    self.tile_folder = tile_folder
    self.info_file = os.path.join(tile_folder, 'info.json')
    self.zoom_levels_file = os.path.join(tile_folder, 'zoom-levels.json')
    self.tiles_zoom_folder = os.path.join(tile_folder, str(level))

    self.image = None
    self.cropped_image = None

  def set_info(self):
    with open(self.info_file) as f:
      self.info = json.load(f)

  def set_zoom_levels(self):
    with open(self.zoom_levels_file) as f:
      self.zoom_levels = json.load(f)

  def get_crop_bounds(self):
    '''
    Returns the four corners of the actual image from the stitched image
    '''
    x, y = self.get_margins()
    return (x, y, x+self.width, y+self.height)

  def get_rows_columns(self):
    '''
    Since tile files are named col_row.jpg, we can optimize
    by onlly stitching together the tiles needed to form the picture
    '''
    start_r = int(math.floor(float(self.y)/self.tile_size))
    start_c = int(math.floor(float(self.x)/self.tile_size))
    
    image_width = float(self.zoom_levels[self.level]["width"])
    image_height = float(self.zoom_levels[self.level]["height"])
    max_row = int(math.ceil(float(image_height) / self.tile_size)) - 1
    max_col = int(math.ceil(float(image_width) / self.tile_size)) - 1

    end_r = min(
              int(math.floor(float(self.y + self.height)/self.tile_size)),
              max_row
            )

    end_c = min(
              int(math.floor(float(self.x + self.width)/self.tile_size)),
              max_col
            )

    return (start_c, end_c, start_r, end_r)

  def get_margins(self):
    '''
    Returns the left margin and top margin to be cropped out
    after the image is stitched together
    Returns (left margin, top margin)
    '''
    return (self.x % self.tile_size, self.y % self.tile_size)

  def get_image(self):
    return self.image

  def get_cropped_image(self):
    return self.cropped_image

  def make_image(self):
    self.set_info()
    self.set_zoom_levels()

    if int(self.level) > int(self.info['max_level']):
      raise ValueError("Invalid Zoom Level")

    self.tile_size = self.info['tile_size']
    self.tile_format = self.info['tile_format']

    start_c, end_c, start_r, end_r = self.get_rows_columns()
    temp_width = (end_c - start_c + 1) * self.tile_size
    temp_height = (end_r - start_r + 1) * self.tile_size
    
    im = Image.new('RGB', (temp_width, temp_height), None)
    
    x_coord = 0
    y_coord = 0
    for col_num in range(start_c, end_c + 1):
      for row_num in range(start_r, end_r + 1):
        tile_filename = str(col_num) + '_' + str(row_num) + '.' + self.tile_format
        tile = Image.open(os.path.join(self.tiles_zoom_folder, tile_filename))
        im.paste(tile, (x_coord, y_coord))
        y_coord += tile.size[1]
      y_coord = 0
      x_coord += tile.size[0]

    self.image = im

  def crop_image(self):
    bounds = self.get_crop_bounds()
    im = self.image.crop(bounds)
    self.cropped_image = im
    return im