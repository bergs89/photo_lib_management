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





# Function that calulates the mean squared error (mse) between two image matrices
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


# Function for rotating an image matrix by a 90 degree angle
def rotate_img(image):
    image = np.rot90(image, k=1, axes=(0, 1))
    return image


# Function for printing filename info of plotted image files
def show_file_info(compared_img, main_img):
    print("Duplicate file: " + image_files[main_img] + " and " + image_files[compared_img])


# Function for checking the quality of compared images, appends the lower quality image to the list
def check_img_quality(directory, imageA, imageB, list):
    size_imgA = os.stat(directory + imageA).st_size
    size_imgB = os.stat(directory + imageB).st_size
    if size_imgA > size_imgB:
        add_to_list(imageB, list)
    else:
        add_to_list(imageA, list)


def variance_of_laplacian(image):
    """Blur detection with OpenCV"""
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(cv2.imread(image), cv2.CV_64F).var()


def check_focus_quality(directory, imageA, imageB, list):
    sharpness_img_a = variance_of_laplacian(directory + imageA)
    sharpness_img_b = variance_of_laplacian(directory + imageB)
    if sharpness_img_a > sharpness_img_b:
        delta_sharpness = sharpness_img_a - sharpness_img_b
        sharpness_ratio = delta_sharpness / sharpness_img_a
        if sharpness_ratio > 0.15:
            add_to_list(imageB, list)
    else:
        delta_sharpness = sharpness_img_b - sharpness_img_a
        sharpness_ratio = delta_sharpness / sharpness_img_b
        if sharpness_ratio > 0.15:
            add_to_list(imageA, list)