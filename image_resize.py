import argparse
import os
from exceptions import (
    InvalidResizeParams,
    ImageResizeWarning,
    ResizeParamsLessThanZero
)
from PIL import Image


def change_image_height_width(image_obj, height, width):
    return image_obj.resize((width, height))


def change_image_scale(image_obj, scale):
    orig_image_size = image_obj.size
    new_image_size = tuple(
        int(size_param * scale) for size_param in orig_image_size
    )
    scaled_image = image_obj.resize(new_image_size)
    return scaled_image


def change_image_height(image_obj, height):
    new_image_width = int(
        (height * image_obj.width) // image_obj.height
    )
    return image_obj.resize(
        (new_image_width, height)
    )


def change_image_width(image_obj, width):
    new_image_height = int(
        (width * image_obj.height) // image_obj.width
    )
    return image_obj.resize(
        (width, new_image_height)
    )


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


def resize_image(input, output, width=None, height=None, scale=None):
    image_obj = Image.open(input)
    old_image_filename = os.path.basename(input)

    if width and height:
        resized_image_obj = change_image_height_width(
            image_obj, height, width
        )
    elif scale:
        resized_image_obj = change_image_scale(image_obj, scale)
    elif width:
        resized_image_obj = change_image_width(image_obj, width)
    elif height:
        resized_image_obj = change_image_height(image_obj, height)
    else:
        resized_image_obj = None

    if resized_image_obj is not None:
        save_resized_image(resized_image_obj,old_image_filename, output)
        return True


def get_args():
    parser = argparse.ArgumentParser(
        description='Tool to resize images'
    )
    size_params_group = parser.add_argument_group('Size params:')
    scale_params_group = parser.add_argument_group('Scale params:')
    parser.add_argument(
        '-i', '--input',
        help='Path to image to resize',
        required=True
    )
    parser.add_argument(
        '-o', '--output',
        help='Path where to put processed image',
        default='.'
    )
    size_params_group.add_argument(
        '--width',
        help='Width of target image in pixels',
        type=int
    )
    size_params_group.add_argument(
        '--height',
        help='Height of target image in pixels',
        type=int
    )
    scale_params_group.add_argument(
        '--scale',
        help='Output scale of resized image',
        type=float
    )
    return parser.parse_args()


def check_input_args(args):

    if args.scale and args.height and args.width:
        raise InvalidResizeParams

    elif (args.scale and args.height) or \
            (args.scale and args.width):
        raise InvalidResizeParams

    elif args.height and args.width:
        raise ImageResizeWarning

    elif args.height is not None and args.height <= 0 or \
            args.width is not None and args.width <= 0 or \
            args.scale is not None and args.scale <= 0:
        raise ResizeParamsLessThanZero

    return vars(args)


if __name__ == '__main__':
    raw_args = get_args()
    try:
        cleaned_args = check_input_args(raw_args)
    except InvalidResizeParams:
        exit('You can\'t specify --height and --width params'
             ' alongside with --scale param')
    except ResizeParamsLessThanZero:
        exit('Resize and scale params should be greater than zero')
    except ImageResizeWarning:
        print('Specifying both --height and --width params'
              ' could damage the resized image proportions')
        cleaned_args = vars(raw_args)

    if resize_image(**cleaned_args):
        print('Image resized successfully!')
    else:
        print('An error has occured while resizing image')
