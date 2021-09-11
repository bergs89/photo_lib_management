import skimage.measure
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import imghdr
import argparse
import cv2

from imutils import paths
from pathlib import Path

import lib_photo_analysis

""" 
Duplicate Image Finder (DIF): function that searches a given directory for images and finds duplicate/similar images among them.
Outputs the number of found duplicate/similar image pairs with a list of the filenames having lower resolution.
"""


def compare_images(directory, similarity="high", compression=50):
    """
    directory (str).........folder to search for duplicate/similar images
    show_imgs (bool)........True = shows the duplicate/similar images found in output
                            False = doesn't show found images
    similarity (str)........"high" = searches for duplicate images, more precise
                            "low" = finds similar images
    compression (int).......recommended not to change default value
                            compression in px (height x width) of the images before being compared
                            the higher the compression i.e. the higher the pixel size, the more computational ressources and time required
    """
    # list where the found duplicate/similar images are stored
    duplicates = []
    lower_res = []
    blur_images = []

    imgs_matrix = lib_photo_analysis.create_imgs_matrix(directory, compression)

    # search for similar images
    if similarity == "low":
        ref = 1000
    # search for 1:1 duplicate images
    else:
        ref = 200

    main_img = 0
    compared_img = 1
    nrows, ncols = compression, compression
    srow_A = 0
    erow_A = nrows
    srow_B = erow_A
    erow_B = srow_B + nrows

    while erow_B <= imgs_matrix.shape[0]:
        while compared_img < (len(image_files)):
            # select two images from imgs_matrix
            imgA = imgs_matrix[srow_A: erow_A,  # rows
                   0: ncols]  # columns
            imgB = imgs_matrix[srow_B: erow_B,  # rows
                   0: ncols]  # columns
            # compare the images
            rotations = 0
            while image_files[main_img] not in duplicates and rotations <= 3:
                if rotations != 0:
                    imgB = rotate_img(imgB)
                err = mse(imgA, imgB)
                if err < ref:
                    add_to_list(image_files[main_img], duplicates)
                    add_to_list(image_files[compared_img], duplicates)
                    lib_photo_analysis.check_img_quality(directory, image_files[main_img], image_files[compared_img], lower_res)
                    lib_photo_analysis.check_focus_quality(directory, image_files[main_img], image_files[compared_img], blur_images)
                rotations += 1
            srow_B += nrows
            erow_B += nrows
            compared_img += 1

        srow_A += nrows
        erow_A += nrows
        srow_B = erow_A
        erow_B = srow_B + nrows
        main_img += 1
        compared_img = main_img + 1

    msg = "\n***\n DONE: found " + str(len(duplicates)) + " duplicate image pairs in " + str(
        len(image_files)) + " total images.\n The following files have lower resolution:"
    print(msg)
    duplicates_and_blur = [x for x in duplicates if x in blur_images]
    return set(duplicates), blur_images, duplicates_and_blur, set(lower_res)

# Function that searches the folder for image files, converts them to a matrix
def create_imgs_matrix(directory, compression):
    global image_files
    image_files = []
    # create list of all files in directory
    folder_files = [filename for filename in os.listdir(directory)]

    # create images matrix
    counter = 0
    for filename in folder_files:
        if not os.path.isdir(directory + filename) and imghdr.what(directory + filename):
            img = cv2.imdecode(np.fromfile(directory + filename, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            if type(img) == np.ndarray:
                img = img[..., 0:3]
                img = cv2.resize(img, dsize=(compression, compression), interpolation=cv2.INTER_CUBIC)
                if counter == 0:
                    imgs_matrix = img
                    image_files.append(filename)
                    counter += 1
                else:
                    imgs_matrix = np.concatenate((imgs_matrix, img))
                    image_files.append(filename)
    return imgs_matrix


# Function for appending items to a list
def add_to_list(filename, list):
    list.append(filename)


if __name__ == '__main__':
    directory = Path(r"/home/stefano/Immagini/FotoTest")
    directory = r"/home/stefano/Immagini/FotoTest/"
    duplicates, blur_images, duplicates_and_blur, lower_resolution = compare_images(directory, show_imgs=False, similarity="low", compression=50)



