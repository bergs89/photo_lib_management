import os
import cv2

from pathlib import Path


def get_pictures_in_directory(directory,
                              pictures_list=[],
                              ):
    pictures = keep_pictures(directory)
    images = []
    for imageN in pictures:
        if pictures_list.__len__() > 0:

            if imageN not in pictures_list:
                continue
            else:
                image = cv2.imread(Path(directory, imageN).__str__())
                images.append(image)
    return images


def save_picture(image_path, image):
    if not cv2.imwrite(str(image_path), image):
        raise Exception("Could not write image")
    else:
        print("Pictures saved correctly.")


def find_duplicates(_directory):
    # TODO
    return


def find_blurry(_directory):
    # TODO
    return


def find_duplicate_and_blurry(_directory):
    # TODO
    return [x for x in find_duplicates(_directory) if x in find_blurry(_directory)]


def keep_pictures(_directory):
    images = []
    files_in_directory = os.listdir(_directory)
    for image in files_in_directory:
        if image.endswith(".png") or \
                image.endswith(".jpg") or \
                image.endswith(".PNG") or \
                image.endswith(".JPG"):
            images.append(image)
    return images
