import local
import os
import shutil
import sys

def format():
    # check arg length
    if len(sys.argv) != 4:
        raise ValueError('Expected 4 arguments: <program> <course code> <file title> <number of images>')

    # get image count
    try:
        image_count = int(sys.argv[3])
    except ValueError:
        raise ValueError(f'Failed to convert {sys.argv[3]} to an int. Expected the image count.')

    # check course code
    course_code = sys.argv[1]
    if course_code not in local.COURSES:
        raise ValueError(f'Invalid course code {course_code}, expected on of {list(local.COURSES.keys())}')

    # create project directory
    project_dir = sys.argv[2]
    if not os.path.isdir(f'{local.LATEX_FOLDER}{course_code}/{project_dir}'):
        os.mkdir(f'{local.LATEX_FOLDER}{course_code}/{project_dir}')

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
        to_path = f'{local.LATEX_FOLDER}{course_code}/{project_dir}/{image_new_filename}'
        shutil.copyfile(from_path, to_path)
        return image_new_filename

    images = [process_image(index, image) for index, image in enumerate(images)]

    with open(f'{local.LATEX_FOLDER}{course_code}/{project_dir}/{project_dir}.tex', 'w') as tex_file:
        tex_file.write(project_dir.join(local.COURSES[course_code][0]))
        for image in images:
            tex_file.write(f'\includegraphics[width=1\\textwidth]{{ {image} }}\n\pagebreak\n\n')
        tex_file.write(local.COURSES[course_code][1])

if __name__ == '__main__':
    format()