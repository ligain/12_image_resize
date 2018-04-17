import argparse
import os
from PIL import Image


def get_new_image_filename(old_filename, width, height):
    filename, extension = os.path.splitext(old_filename)
    return '{filename}__{width}x{height}{extension}'.format(
        filename=filename,
        width=width,
        height=height,
        extension=extension
    )


def save_resized_image(image_obj, old_image_filename, path_to_result):
    new_image_filename = get_new_image_filename(
        old_image_filename,
        image_obj.width,
        image_obj.height
    )
    filepath = os.path.join(path_to_result, new_image_filename)
    image_obj.save(filepath)


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

    return size


def validate_size_value(value):
    size_value = int(value)
    if size_value <= 0:
        raise argparse.ArgumentTypeError(
            'Resize params should be greater than zero with type: integer'
        )
    return size_value


def validate_scale_value(value):
    scale_value = float(value)
    if scale_value <= 0.0:
        raise argparse.ArgumentTypeError(
            'Scale param should be greater than zero with type: float'
        )
    return scale_value


def validate_args(parser):
    args = parser.parse_args()

    if not os.path.isfile(args.path_to_image):
        parser.error('Invalid path to target image')

    if not os.path.isdir(args.path_to_result):
        parser.error('Invalid output path')

    if args.scale and args.height and args.width:
        parser.error("You can't specify --height and --width "
                     "params alongside with --scale param")

    if args.scale and (args.height or args.width):
        parser.error("You can't use together --height and "
                     "--scale or --width and --scale params")

    if args.height and args.width:
        print('Specifying both --height and --width params could '
              'damage the resized image proportions')

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
        type=validate_size_value,
        default=0
    )
    size_params_group.add_argument(
        '--height',
        help='Height of target image in pixels',
        type=validate_size_value,
        default=0
    )
    scale_params_group.add_argument(
        '--scale',
        help='Output scale of resized image',
        type=validate_scale_value,
        default=0.0
    )

    validated_args = validate_args(parser)

    return validated_args


if __name__ == '__main__':
    args = get_args()

    image = Image.open(args.path_to_image)
    new_image_size = calc_new_image_size(
        image.width,
        image.height,
        width=args.width,
        height=args.height,
        scale=args.scale
    )
    resized_image = image.resize(new_image_size)
    old_image_filename = os.path.basename(image.filename)
    save_resized_image(resized_image, old_image_filename, args.path_to_result)
    print('Image resized successfully!')
