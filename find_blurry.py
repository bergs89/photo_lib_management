import cv2
import os


class Blurry(object):

    def __init__(self, _imageA, _imageB, ):
        self.imageA = _imageA
        self.imageB = _imageB
        return

    def __variance_of_laplacian(image):
        """Blur detection with OpenCV"""
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(cv2.imread(image), cv2.CV_64F).var()

    def find_blurry(self,):
        sharpness_img_a = self.__variance_of_laplacian(self.imageA)
        sharpness_img_b = self.__variance_of_laplacian(self.imageB)

        if sharpness_img_a > sharpness_img_b:
            delta_sharpness = sharpness_img_a - sharpness_img_b
            sharpness_ratio = delta_sharpness / sharpness_img_a
            if sharpness_ratio > 0.15:
                blurry = (False, True)
            else:
                blurry = (False, False)
        else:
            delta_sharpness = sharpness_img_b - sharpness_img_a
            sharpness_ratio = delta_sharpness / sharpness_img_b
            if sharpness_ratio > 0.15:
                blurry = (True, False)
            else:
                blurry = (False, False)
        return blurry