import local
import os
import shutil
import sys

# check arg length
if len(sys.argv) != 3:
    raise ValueError('Expected 3 arguments: <program> <optional file title> <number of images>')

# get image count
try:
    image_count = int(sys.argv[2])
except ValueError:
    raise ValueError('Failed to convert {sys.argv[2]} to an int. Expected the image count.')

# create project directory
project_dir = sys.argv[1]
if not os.path.isdir(f'{local.FILE_FOLDER}{project_dir}'):
    os.mkdir(f'{local.FILE_FOLDER}{project_dir}')

# copy images to project directory
image_folder_contents = sorted(os.listdir(local.IMAGE_FOLDER), key=lambda filename: os.path.getctime(f'{local.IMAGE_FOLDER}{filename}'))

images = []
for image in image_folder_contents[::-1]:
    if len(images) == image_count:
        break
    if image.startswith('.'):
        # do not count non-visible files,
        # typically auto generated
        continue
    images.append(image)

# reverse to put most recent photos last
images = images[::-1]

def process_image(index, image):
    from_path = f'{local.IMAGE_FOLDER}{image}'
    image_extension = image.split('.')[-1]
    image_new_filename = f'image_{index}.{image_extension}'
    to_path = f'{local.FILE_FOLDER}{project_dir}/{image_new_filename}'
    shutil.copyfile(from_path, to_path)
    return image_new_filename

images = [process_image(index, image) for index, image in enumerate(images)]

with open(f'{local.FILE_FOLDER}{sys.argv[1]}/{sys.argv[1]}.tex', 'w') as tex_file:
    tex_file.write(local.TEX_HEADER)
    for image in images:
        tex_file.write(f'\includegraphics[width=1\\textwidth]{{ {image} }}\n\pagebreak\n\n')
    tex_file.write(local.TEX_FOOTER)