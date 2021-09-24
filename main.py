import utils
import os

from pathlib import Path
from panorama import Panorama


def preprocess_pictures2import(_directory,
                               find_duplicates=True,
                               find_blurry=True, make_panoramas=True,
                               find_panorama_candidates=True,
                               delete_duplicates_and_blurry=False,
                               ):
    if find_duplicates:
        duplicate_pictures = utils.find_duplicates(_directory)

    if find_duplicates and find_blurry:
        duplicate_and_blurry = utils.find_duplicate_and_blurry(_directory)

    if make_panoramas:
        if find_panorama_candidates:
            panorama_pictures_list = Panorama(_directory, _images=None).find_pictures_for_panorama()
            panoramas_pictures = utils.get_pictures_in_directory(_directory, pictures_list=panorama_pictures_list)
            index = 0
            for panorama_pictures in panoramas_pictures:
                panorama = Panorama(_directory, _images=panorama_pictures).make_panorama()
                panorama_picture_name = f'Panorama_{index}_.jpg'.format(index=index)
                panorama_path = Path(_directory, panorama_picture_name)
                utils.save_picture(panorama_path, panorama)
                index =+ 1
        else:
            panorama_pictures = utils.get_pictures_in_directory(_directory)
            panorama = Panorama(_directory, _images=panorama_pictures).make_panorama()
            panorama_path = Path(_directory, 'Panorama.jpg')
            utils.save_picture(panorama_path, panorama)

    if delete_duplicates_and_blurry:
        for pic in duplicate_and_blurry:
            pic_path = Path(_directory, pic)
            os.remove(pic_path)


if __name__ == '__main__':
    directory = Path(r'C:\Users\SBE2346\Desktop\Stitch\Pictures\2')
    preprocess_pictures2import(directory)
