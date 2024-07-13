from typing import List, Tuple
import os
from PIL import Image

def from_rgb(rgb: Tuple[int, int, int]) -> str:
    """
    translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 


def is_image(filename: str) -> bool:
    suffixes = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]
    for suffix in suffixes:
        if filename.endswith(suffix):
            return True
    return False


def get_all_image_paths(images_directory: str) -> List[str]:
    """
    Return all images paths in :images_directory: and its subdirectories
    """
    image_paths = []
    for root, dirs, files in os.walk(images_directory):
        for file in files:
            if is_image(file):
                image_paths.append(os.path.join(root, file))
    return image_paths


def get_image_caption(image_path: str) -> str:
    basename = os.path.basename(image_path)
    caption = ".".join(basename.split(".")[:-1]) # Remove the extension
    caption = caption.replace("_", " ") # Replace underscores with spaces
    return caption


def resize_image(image: Image, max_dimensions: Tuple[int, int]) -> Image:
    """
    Resize the image *image* to fit within the frame dimensions *max_dimensions* if it is larger or heigher
    """
    image_dimensions = image.size
    if image_dimensions[0] > max_dimensions[0]:
        ratio = max_dimensions[0] / image_dimensions[0]
        new_dimensions = (int(image_dimensions[0] * ratio), int(image_dimensions[1] * ratio))
        image = image.resize(new_dimensions)

    if image_dimensions[1] > max_dimensions[1]:
        ratio = max_dimensions[1] / image_dimensions[1]
        new_dimensions = (int(image_dimensions[0] * ratio), int(image_dimensions[1] * ratio))
        image = image.resize(new_dimensions)
    return image
