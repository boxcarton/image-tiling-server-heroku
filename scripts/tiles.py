import shutil
import math
import json
import os
from PIL import Image

class ImageTiles(object):
  def __init__(self, src_file, tile_size, tile_format):
    self.image = Image.open(src_file)   
    self.image_width = self.image.size[0]
    self.image_height = self.image.size[1]

    self.tile_size = int(tile_size)
    self.tile_format = tile_format

    self.num_levels = self.calc_num_levels()
    self.resize_filter = Image.ANTIALIAS #antialias is best, might let users to set

    self.info = {} #information about image tiles
    self.zoom_levels = {} #image size information at each level

  def calc_num_levels(self):
    max_dimension = max(self.image_width, self.image_height)
    self.num_levels = int(math.ceil(math.log(max_dimension, 2))) + 1
    return self.num_levels

  def get_scale_at_level(self, level):
    self.max_level = self.num_levels - 1
    return math.pow(0.5, self.max_level - level)

  def get_dimensions_at_level(self, level):
    '''Returns image dimension at each level'''
    scale = self.get_scale_at_level(level)
    width = int(math.ceil(self.image_width * scale))
    height = int(math.ceil(self.image_height * scale))
    return (width, height)

  def get_num_tiles_at_level(self, level):
    width, height = self.get_dimensions_at_level(level)
    return (int(math.ceil(float(width) / self.tile_size)),
            int(math.ceil(float(height) / self.tile_size)))

  def get_image_at_level(self, level):
    width, height = self.get_dimensions_at_level(level)
    return self.image.resize((width, height), self.resize_filter)

  def get_tiles_at_level(self, level):
    '''Returns a generator for iterating through the potential tiles'''
    columns, rows = self.get_num_tiles_at_level(level)
    for column in xrange(columns):
      for row in xrange(rows):
        yield (column, row)

  def get_tile_bounds_at_level(self, level, column, row):
    x = (column * self.tile_size)
    y = (row * self.tile_size)

    level_width, level_height = self.get_dimensions_at_level(level)
    w = min(self.tile_size, level_width  - x)
    h = min(self.tile_size, level_height - y)
    return (x, y, x + w, y + h)

  def create_dest_folder(self, path):
    '''Removes folder if already exists, creates if not'''
    if os.path.exists(path):
      shutil.rmtree(path)
      os.makedirs(path)
    else:
      os.makedirs(path)
    return path

  def create_tiles(self, dest):
    dest_folder = self.create_dest_folder(dest)
    for level in xrange(self.num_levels):
      level_folder = self.create_dest_folder(os.path.join(dest_folder, str(level)))
      level_image = self.get_image_at_level(level)
      
      #save dimension info at each zoom level
      w, h = self.get_dimensions_at_level(level)
      self.zoom_levels[level] = {
        'width': w,
        'height': h,
      }

      for (column, row) in self.get_tiles_at_level(level):
        bounds = self.get_tile_bounds_at_level(level, column, row)
        tile = level_image.crop(bounds)
        tile_path = os.path.join(level_folder,
                     '%s_%s.%s'%(column, row, self.tile_format))
        tile_file = open(tile_path, 'wb')
        if self.tile_format == 'jpg':
          tile.save(tile_file, 'JPEG', quality=100)
        else:
          tile.save(tile_file)

    self.info["tile_format"] = self.tile_format
    self.info["max_level"] = self.max_level
    self.info["tile_size"] = self.tile_size
    with open(os.path.join(dest_folder, 'info.json'),'w') as f:
      f.write(json.dumps(self.info))

    with open(os.path.join(dest_folder, 'zoom-levels.json'),'w') as f:
      f.write(json.dumps(self.zoom_levels))