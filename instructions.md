# Image Tiling Server for Large Images

## Overview

In Biology, specifically microscopy, it is quite common to generate extremely large images.
Downloading these images becomes impractical as the number of downloads increases. 
A better approach is to allow the user to pan and zoom around this mega-image so that
only part of the image needs to be downloaded.

Your task is to build a server that allows a user to query for a specific region of
the photo at a specified ZoomLevel - just like Google Maps.

Assuming that these images might not fit into memory, you must first preprocess the image
and create a TileSet for each ZoomLevel for quicker loading.  TileSet and ZoomLevel
are defined below.

Here is a large example image:

  [hubble](http://imgsrc.hubblesite.org/hu/db/images/hs-2015-02-a-full_jpg.jpg)

Please feel free to write this server in whatever language you are most comfortable.
We are interested in seeing your coding style and structure.

## Definitions

- ZoomLevel:
    An integer identifier that is used to choose which TileSet to
    query from.  The lower the ZoomLevel the lower the resolution
    of the TileSet image.

- Tile:
    A rectangular subsection of an image uniquely identified by its 
    ZoomLevel, width, height and origin.  By stitching together all
    of the tiles at a given ZoomLevel the original image can be recreated.

- TileSet:
    A collection of tiles that can be used to stitch together
    any portion of the image.

## Requirements

1. A script that transforms a given image into a set of tile images.
   It is perfectly fine to use image processing libraries, but
   please avoid using any image tiling software.
   
       ```
       example command: 
         ./create_tiles super_large.png
       ```

2. A web server with the given endpoints:

   GET /zoom-levels

   - Returns width and height information, in pixels, for each zoom 
   
       ```
       {
         '0': {width: 625,    height: 625},
         '1': {width: 1250,   height: 1250},
         '2': {width: 2500,   height: 2500},
         '3': {width: 5000,   height: 5000},
         '4': {width: 10000,  height: 10000}
       }
       ```


   GET /tile?x=2000&y=3300&width=800&height=600&zoom=3

   - Returns an image of the width and height specified where
     the top-left pixel of the returned image corresponds to pixel (x,y)
     at the specified ZoomLevel.

     In the example above, the returned image would be:
       - 800px wide
       - 600px tall
       - (0,0) pixel corresponds to (2000,3300) pixel at ZoomLevel 3.

   - Parameters: (The origin is the top left of the image)
       - x: number  pixels width-wise from the origin
       - y: number opixels height-wise from the origin
       - width: number  pixels wide of the returned image
       - height: number  pixels tall of the returned image
       - zoom: The tileset to use. A higher zoom means closer.

## NOTES

  - All API endpoints should respond within 250ms.
