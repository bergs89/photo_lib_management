import numpy as np
import os
import cv2
import pandas as pd


from find_duplicates import Duplicates
from find_blurry import Blurry



def load_image(path):
    return cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_UNCHANGED)


def resize_image(image, compression):
    return cv2.resize(image, dsize=(compression, compression), interpolation=cv2.INTER_CUBIC)


# Function that calulates the mean squared error (mse) between two image matrices
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


# Function for rotating an image matrix by a 90 degree angle
def rotate_img(image):
    image = np.rot90(image, k=1, axes=(0, 1))
    return image


def make_df(path, ):
    df = pd.DataFrame()

    paths = find_files(path)
    df['paths'] = paths

    duplicates = []
    for file in paths:
        col_name = 'duplicate' + str(file)
        for second_file in paths:
            duplicate = Duplicates(file, second_file).find_duplicates(similarity="low")
            duplicates.append(duplicate)
        df[col_name] = duplicates

    return df


def update_df_blurry(path, df, ):
    paths = find_files(path)

    blurred = []
    for file in paths:
        duplicate_col_name = 'duplicate' + str(file)
        col_name = 'blurred' + str(file)
        for second_file in paths:
            if df[duplicate_col_name].loc[second_file] is True:
                blurry = Blurry(file,second_file).find_blurry()
                blurred.append(blurry[1])

        df[col_name] = blurred
    return df


def find_files(path):
    return [os.path.join(dp, f) for dp, dn, fn in os.walk(path) for f in fn]


