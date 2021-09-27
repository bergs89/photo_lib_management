import cv2
import os
import lib_photo_analysis

from pathlib import Path

class Duplicates(object):

    def __init__(self, _imageA, _imageB, similarity="low", ):
        self.imageA = _imageA
        self.imageB = _imageB
        self.similarity = similarity
        return

    def find_duplicates(self, similarity="low", ):
        imgA_path = self.imageA
        imgB_path = self.imageB
        if similarity == "low":
            ref = 1000
        # search for 1:1 duplicate images
        else:
            ref = 200
        list_images_path = [imgA_path, imgB_path]

        images = []
        for image_path in list_images_path:
            image = lib_photo_analysis.load_image(image_path)
            resized_image = lib_photo_analysis.resize_image(image, compression=50)
            images.append(resized_image)
        imgA = images[0]
        imgB = images[1]

        duplicates = False
        rotations = 0
        while not duplicates and rotations <= 3:
            if rotations != 0:
                imgB = lib_photo_analysis.rotate_img(imgB)
            err = lib_photo_analysis.mse(imgA, imgB)
            if err < ref:
                duplicates = True
            rotations += 1
        return duplicates
