from threading import local
from PIL import Image
from colorthief import ColorThief
import requests
import shutil
import os
import hashlib

import config


"""
Download a remote file
:param url: URL to remote file
:param local_filename: Local path to write to
"""
def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


"""
Download a remote file, hashname + resize, then get dominant palette
Used for waifu image metadata
:param waifu_name: Name of the waifu
:param url: URL to remote file
:return valid, local_filename, palette, size
    valid      - boolean, if False image failed to download / isn't a real image
    local_file - hashed file path of resized image
    palette    - Array of RGB tuple of dominant colors in image
    size       - Tuple (w, h) of image
"""
def download_image_and_palette(waifu_name, url):
    valid = True
    local_filename = f"{waifu_name[:16]}_{hashlib.md5(url.encode()).hexdigest()[0:16]}.png" \
        .replace("/", "").replace("\\", "")
    out = os.path.join(config.IMAGE_OUTPUT_DIR, local_filename)
    palette = []
    size = (-1, -1)

    os.makedirs(config.IMAGE_OUTPUT_DIR, exist_ok=True)

    try:
        if not os.path.exists(out):
            download_file(url, "temp.png")
            im1 = Image.open("temp.png")
            width = round(im1.width / im1.height * config.THUMBNAIL_HEIGHT)

            im_small = im1.resize((width, config.THUMBNAIL_HEIGHT), Image.ANTIALIAS)
            im_small.save(out)

        size = Image.open(out).size
        color_thief = ColorThief(out)
        palette = color_thief.get_palette(color_count=config.PALETTE_SIZE)
    except Exception as e:
        print(f"Error downloading image:\n{e}")
        valid = False

    if os.path.exists("temp.png"):
        os.remove("temp.png") # Delete temp file

    return valid, local_filename, palette, size
