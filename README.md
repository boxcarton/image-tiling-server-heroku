# Image Tiling Server

A script to break large images into smaller tiles at various zoom levels.

A Flask server to serve these files

## Usage

#### To create image tiles
```python
./script/create_tiles.py [path_source_image]
```

## API

#### GET zoom-levels

_Returns width and height information, in pixels, for each zoom_
   


Ex:
   ```
   {
     '0': {width: 625,    height: 625},
     '1': {width: 1250,   height: 1250},
     '2': {width: 2500,   height: 2500},
     '3': {width: 5000,   height: 5000},
     '4': {width: 10000,  height: 10000}
   }
   ```

#### GET tile?x=x_offset&y=y_offset&width=image_width&height=image_height&zoom=zoom_level

_Returns an image of the width and height specified where
     the top-left pixel of the returned image corresponds to pixel (x,y)
     at the specified ZoomLevel._

Ex:
```
     GET /tile?x=2000&y=3300&width=800&height=600&zoom=3
     returns an image that's:
       - 800px wide
       - 600px tall
       - (0,0) pixel corresponds to (2000,3300) pixel at ZoomLevel 3.
```
   - Parameters: (The origin is the top left of the image)
       - x: number  pixels width-wise from the origin
       - y: number opixels height-wise from the origin
       - width: number  pixels wide of the returned image
       - height: number  pixels tall of the returned image
       - zoom: The tileset to use. A higher zoom means closer._