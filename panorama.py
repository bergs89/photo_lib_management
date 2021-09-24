import cv2
import os


class Panorama(object):

    def __init__(self, _directory, _images):
        self.directory = _directory
        self.images = _images
        return

    def make_panorama(self):
        status, panorama = cv2.Stitcher.create().stitch(self.images)

        # TODO
        # if status:
        #     return panorama
        # else:
        #     raise Exception("Could not stitch the panorama")

        # TODO
        # crop panos to make it rectangular
        return panorama

    def find_pictures_for_panorama(self):
        # TODO
        # check if pictures are similar in some cropping portion
        # return the list
        return [x for x in os.listdir(self.directory) if x.endswith(".jpg")]