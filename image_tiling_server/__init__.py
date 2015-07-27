from flask import Flask

app = Flask(__name__)

app.config.from_object('image_tiling_server.settings')
app.url_map.strict_slashes = False

import image_tiling_server.controllers