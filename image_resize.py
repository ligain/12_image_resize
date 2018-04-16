import argparse
import os
from PIL import Image


def get_new_image_filename(old_filename, image_width, image_height):
    old_filename, old_extension = os.path.splitext(old_filename)
    return '{filename}__{width}x{height}{extension}'.format(
        filename=old_filename,
        width=image_width,
        height=image_height,
        extension=old_extension
    )


def save_resized_image(image_obj, old_image_filename, path_to_result):
    new_image_filename = get_new_image_filename(
        old_image_filename,
        image_obj.width,
        image_obj.height
    )
    filepath = os.path.join(path_to_result, new_image_filename)
    image_obj.save(filepath)


def open_image(path_to_image):
    image_obj = Image.open(path_to_image)
    return image_obj


def calc_new_image_size(orig_width, orig_height,
                        width=None, height=None, scale=None):
    """
    Calculates new image size and returns tuple (width, height)
    """

    if width and height:
        size = (width, height)
    elif scale:
        size = (
            int(orig_width * scale),
            int(orig_height * scale)
        )
    elif width:
        size = (
            width,
            int((width * orig_height) // orig_width)
        )
    elif height:
        size = (
            int((height * orig_width) // orig_height),
            height
        )
    else:
        size = (orig_width, orig_height)

    return size


def resize_image(image_obj, width, height):
    new_image_size = calc_new_image_size(width, height)
    resized_image_obj = image_obj.resize(new_image_size)
    return resized_image_obj


def validate_args(parser):
    args = parser.parse_args()

    if not os.path.isfile(
            os.path.expanduser(args.path_to_image)):
        parser.error('Invalid path to target image')
    if not os.path.exists(
            os.path.expanduser(args.path_to_result)):
        parser.error('Invalid output path')
    elif args.scale and args.height and args.width:
        parser.error("You can't specify --height and --width "
                     "params alongside with --scale param")
    elif (args.scale and args.height) or (args.scale and args.width):
        parser.error("You can't use together --height and "
                     "--scale or --width and --scale params")
    elif args.height and args.width:
        print('Specifying both --height and --width params could '
              'damage the resized image proportions')
    elif any([args.height < 0, args.width < 0, args.scale < 0]):
        parser.error('Resize and scale params should be greater than zero')

    return args


def get_args():
    parser = argparse.ArgumentParser(
        description='Tool to resize images'
    )
    size_params_group = parser.add_argument_group('Size params:')
    scale_params_group = parser.add_argument_group('Scale params:')
    parser.add_argument(
        '-t', '--target-image',
        help='Path to image to resize',
        dest='path_to_image',
        required=True
    )
    parser.add_argument(
        '-o', '--output-path',
        help='Path where to put processed image',
        dest='path_to_result',
        default='.'
    )
    size_params_group.add_argument(
        '--width',
        help='Width of target image in pixels',
        type=int,
        default=0
    )
    size_params_group.add_argument(
        '--height',
        help='Height of target image in pixels',
        type=int,
        default=0
    )
    scale_params_group.add_argument(
        '--scale',
        help='Output scale of resized image',
        type=float,
        default=0.0
    )

    validated_args = validate_args(parser)

    return validated_args


if __name__ == '__main__':
    args = get_args()

    image = open_image(args.path_to_image)
    new_image_size = calc_new_image_size(
        image.width,
        image.height,
        width=args.width,
        height=args.height,
        scale=args.scale
    )
    resized_image = resize_image(image, *new_image_size)
    old_image_filename = os.path.basename(image.filename)
    save_resized_image(resized_image, old_image_filename, args.path_to_result)
    print('Image resized successfully!')
