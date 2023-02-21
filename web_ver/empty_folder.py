import glob
import os


def delete_images():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
