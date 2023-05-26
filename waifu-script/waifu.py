import sys
import json

from textwrap import wrap
from image import download_image_and_palette


"""
If object is not a list wrap it (return [obj])
:param obj: Obj to wrap
:returns: Obj or wrapped obj
"""
def wrap_as_list(obj):
    if type(obj) != list:
        return [obj]
    return obj


"""
A waifu object
:param Bowserinator:
"""
class Waifu(object):
    """
    :param yaml_doc: Decoded YAML document object for waifu
    """
    def __init__(self, yaml_doc):
        if not "name" in yaml_doc or "series" not in yaml_doc or "images" not in yaml_doc:
            print(f"Missing required properties ('name', 'series' and 'images') for {yaml_doc}")
            sys.exit(1)

        self.name = yaml_doc['name'].strip()
        self.series = yaml_doc['series']
        self.age = yaml_doc.get('age', [-1])
        self.nicknames = yaml_doc.get('nicknames', [])
        self.gender = yaml_doc.get('gender', 'F').upper()
        self.height = yaml_doc.get('height', 'Unknown')
        self.rank = yaml_doc.get('rank', '?').upper()
        self.images = yaml_doc.get('images', [])
        self.birthday = yaml_doc.get('birthday', 'Unknown')
        self.tags = yaml_doc.get('tags', [])
        self.palette = []

        self.series = wrap_as_list(self.series)
        self.age = wrap_as_list(self.age)
        self.nicknames = wrap_as_list(self.nicknames)
        self.images = wrap_as_list(self.images)
        self.tags = wrap_as_list(self.tags)

        if self.rank not in "?ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            print(f"Invalid rank for {self.name} (Got '{self.rank}', requires '?' or alpha)")
            sys.exit(1)
        if self.gender not in ["M", "F", "MF", "FM", "U"]:
            print(f"Invalid gender for {self.name} (Got '{self.gender}', accepts only M/F/MF/FM/U")
            sys.exit(1)
        self.download_images()

    """
    Download all images to dir specified in config
    Also generate self.palette and remove invalid images from self.images
    """
    def download_images(self):
        new_images = []
        im_sizes = []
        for image in self.images:
            valid, name, palette, size = download_image_and_palette(self.name, image)
            if not valid:
                print(f"Error downloading {image}")
                continue

            new_images.append(name)
            self.palette.append(palette)
            im_sizes.append(size)
        self.images = new_images
        self.im_sizes = im_sizes

    """
    Get CSV headers, must match __str__
    """
    @staticmethod
    def headers():
        return "name,series,age,nicknames,height,rank,images,birthday,tags,palette,gender,im_sizes"

    """
    Convert to a JSON list style string
    :returns: Formatted string
    """
    def __str__(self):
        out = [self.name, self.series, self.age, self.nicknames, self.height, self.rank, self.images, self.birthday, self.tags, self.palette, self.gender, self.im_sizes]
        return json.dumps(out, separators=(',', ':'))

