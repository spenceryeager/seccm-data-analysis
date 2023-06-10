# this will take the image director from current_voltage_movie.py and merge it into a video
import cv2
import os
import numpy as np


def main():
    filepath = r"R:\Spencer Yeager\data\NiOx_Project\2023\05_May\13May2023_JuanNiOx_500nmTip\frames"
    movie_outputpath = r"R:\Spencer Yeager\data\NiOx_Project\2023\05_May\13May2023_JuanNiOx_500nmTip\movie1"
    moviename = "movie.mp4"
    image_merge(filepath, os.path.join(movie_outputpath, moviename))


def image_merge(filepath, movie_outputpath):
    imlist = os.listdir(filepath)
    fileno = len(imlist)
    # print(fileno)
    frameno = np.arange(0, fileno, 1)
    print(frameno)
    first_imagepath = os.path.join(filepath, make_image_name(0))
    frame = cv2.imread(first_imagepath)
    cv2.imshow('video', frame)
    height, width, channels = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    out = cv2.VideoWriter(movie_outputpath, fourcc, 60.0, (width, height))
    
    for number in frameno:
        make_image_name(number)
        framepath = os.path.join(filepath, make_image_name(number))
        frame = cv2.imread(framepath)
        out.write(frame)
        cv2.imshow('video', frame)
    
    out.release()
    cv2.destroyAllWindows()


def make_image_name(frameno):
    framename = str(frameno) + ".png"
    return framename


if __name__ == "__main__":
    main()
