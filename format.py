import local
import os
import sys

if len(sys.argv) != 3:
    raise ValueError('Expected 3 arguments: <program> <optional file title> <number of images>')

try:
    image_count = int(sys.argv[2])
except ValueError:
    raise ValueError('Failed to convert {sys.argv[2]} to an int. Expected the image count.')

image_folder_contents = sorted(os.listdir(local.IMAGE_FOLDER), key=lambda filename: os.path.getctime(f'{local.IMAGE_FOLDER}{filename}'))
images = image_folder_contents[-image_count:]

with open(f'{local.IMAGE_FOLDER}{sys.argv[1]}') as tex_file:
    pass