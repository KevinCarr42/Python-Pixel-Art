# Image to Pixel Art Converter

A Python tool that converts photos into pixel art using custom color palettes.

<img src="example/example.gif" width="1000">


This example image uses a photograph by [Harrison Haines](https://www.pexels.com/@harrisonhaines/), available under the [Pexels License](https://www.pexels.com/license/).
Source: [Skyline Photography of Buildings during Nighttime](https://www.pexels.com/photo/skyline-photography-of-buildings-during-nighttime-2973098/)

## Features

- Converts images to pixelated, posterized art
- Uses custom color palettes (cyan/magenta palette included)
    - [garbage.html](garbage.html) is only included to use the colour picker in PyCharm
- Optional cropping to match output aspect ratio
- Optional blur before posterization for smoother results

## Usage

```python
from image_processing import posterize_pixelate
import palettes

posterize_pixelate(
    'input.jpg',
    img_output_path='output.png',
    w_out=640,
    h_out=360,
    palette=palettes.cyan_magenta_palette,
    crop=True
)
```

## Files

- `image_processing.py` - Main processing functions
- `palettes.py` - Color palette definitions
- `garbage.html` - Color picker utility for PyCharm
- `example/example.gif` - Before/after demo

## Requirements

- PIL / Pillow
- NumPy
