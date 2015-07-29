import os
import StringIO
import json
from flask import Flask, request
from flask import send_file, jsonify

from image_tiling_server.image import ImageMaker
from image_tiling_server import app

class InvalidRequest(Exception):
  def __init__(self, message, status_code=None, payload=None):
      Exception.__init__(self)
      self.message = message
      if status_code is not None:
          self.status_code = status_code
      self.payload = payload

  def to_dict(self):
      rv = dict(self.payload or ())
      rv['message'] = self.message
      return rv

@app.route('/zoom-levels', methods=['GET'])
def get_zoom_levels():
  tile_folder = app.config['TILE_FOLDER']
  zoom_file = os.path.join(tile_folder, 'zoom-levels.json')
  with open(zoom_file) as f:
    zoom_levels = json.load(f)

  return jsonify(zoom_levels), 200

@app.route('/tile', methods=['GET'])
def make_tile():
  x = request.args.get('x', '')
  y = request.args.get('y', '')
  width = request.args.get('width', '')
  height = request.args.get('height', '')
  level = request.args.get('zoom', '')
  tile_folder = app.config['TILE_FOLDER']

  #grab zoom-level.json and info.json
  tile_folder = app.config['TILE_FOLDER']
  zoom_file = os.path.join(tile_folder, 'zoom-levels.json')
  info_file = os.path.join(tile_folder, 'info.json')
  with open(zoom_file) as f:
    zoom_levels = json.load(f)
  with open(info_file) as f:
    info = json.load(f)

  #check for invalid requests
  if level not in zoom_levels.keys():
    raise InvalidRequest("Zoom level does not exist.", 
                         status_code=400)

  image_width = int(zoom_levels[level]['width'])
  image_height = int(zoom_levels[level]['height'])
  file_format = info['tile_format']

  if int(x) < 0 or int(y) < 0 or \
     int(x) > image_width or int(y) > image_height:
    raise InvalidRequest("Offset out of range.",
                         status_code=400)

  if int(width) > image_width or int(height) > image_height:
    raise InvalidRequest("Requested image too large for zoom level.", 
                         status_code=400)

  if int(x) + int(width) > image_width or \
     int(y) + int(height) > image_height:
    raise InvalidRequest("Requested image is out of range.", 
                         status_code=400)

  im = ImageMaker(level, x, y, width, height, tile_folder)
  im.make_image()
  cropped_im = im.crop_image()

  img_io = StringIO.StringIO()
  
  if file_format == 'jpg':
    cropped_im.save(img_io, 'JPEG', quality=100)
  else:
    cropped_im.save(img_io, file_format)
  mimetype = "image/"+file_format

  img_io.seek(0)
  return send_file(img_io, mimetype=mimetype)

@app.errorhandler(InvalidRequest)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response