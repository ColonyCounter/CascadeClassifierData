#!/usr/bin/env python

from os import listdir
from sys import argv
from PIL import Image

def create_bg_file(path, filenames):
    print("[*] Creating bg file...")
    file_path = path + "bg.txt"
    img_path = path + "neg/"
    with open(file_path, "w") as f:
        for img in filenames:
            str_to_write = "neg/" + img + "\n"

            f.write(str_to_write)
            print("\tAdded: ", str_to_write, end="")

def create_positive_file(path, filenames):
    print("[*] Creating positive file...")
    print("\tAssuming object covers the whole picture and just one object...")

    # only add if it contains just one object!
    file_path = path + "info.dat"
    img_path = path + "pos/"
    with open(file_path, "w") as f:
        for img in filenames:
            next_img = img_path + img
            size = get_image_size(next_img)
            str_to_write = "pos/" + img + " 1" + " 0 0 " + str(size[0]) + " " + str(size[1]) + "\n"

            f.write(str_to_write)
            print("\tAdded: ", str_to_write, end="")

def get_image_size(img_path):
    with Image.open(img_path) as im:
        return im.size

def get_all_png_files(dir_path):
    print("[*] Getting all png files at: ", dir_path)
    png_files = []
    for f in listdir(dir_path):
        if f.endswith(".png"):
            png_files.append(f)
            print("Found: ", f)

    return png_files

def get_all_jpg_files(dir_path):
    print("[*] Getting all jpg files at: ", dir_path)
    jpg_files = []
    for f in listdir(dir_path):
        if f.endswith(".jpg") or f.endswith(".jpeg"):
            jpg_files.append(f)
            print("\tFound: ", f)

    return jpg_files

def get_mean_size(dir_path, filenames):
    print("[*] Getting mean size of images...")
    sum_width = 0
    sum_height = 0
    img_count = 0
    mean_width = 0
    mean_height = 0

    for filename in filenames:
        img_path = dir_path + filename
        size = get_image_size(img_path)
        sum_width += size[0]
        sum_height += size[1]
        img_count += 1

    if img_count < 1:
        print("[!] Error in get_mean_size: No images given.")
        return(1)

    mean_width = sum_width / img_count
    mean_height = sum_height / img_count
    print("\tMean in (width, height)")
    print("\tFloat:   ({}, {})".format(mean_width, mean_height))
    print("\tInteger: ({}, {})".format(round(mean_width), round(mean_height)))

    return [round(mean_width), round(mean_height)]


def resize_images(path, dir_path, filenames, new_size):
    print("[*] Resizing positive images...")
    print("\tNew size is:", new_size)
    # do not overwrite images
    # writes new images in pos_resized, only resizing positive images right now
    for filename in filenames:
        img_path = dir_path + filename
        img_new_path = path + "pos_resized/" + filename
        with Image.open(img_path) as img_in:
            img_out = img_in.resize(new_size)
            img_out.save(img_new_path)

    print("\tFinished resizing.")

if __name__ == "__main__":
    print("simplefilecreator.py")

    print("Usage: ")
    print("\tsimplefilecreator -g jpg -p /home/me/Pictures/ -f + -w 25 -h 25")
    print("\t-g: jpg or png")
    print("\t-p: path to dir")
    print("\t-f: + for positive images or - for bg")
    print("\t-w: width that images should be resized to")
    print("\t-h: height that images should be resized to")
    print("\t-m: resize to mean size value of images")
    # enable resize or cropping, currently just resizing

    print("Positive images are stored in /home/$USER/Pictures/pos/\nThe pos/ dir is added automatically to your path")

    if len(argv) < 7:
        print("[!] Error: Not enough information given. Please restart service.")
        exit(1)

    image_type = None
    path = None
    make_bg = False
    resize = False
    resize_with_mean = False
    width = 0
    height = 0

    for i in range(len(argv)):
        if argv[i] == "-g":
            image_type = argv[i+1]
        elif argv[i] == "-p":
            path = argv[i+1]
            if not path.endswith("/"):
                path = path + "/"
        elif argv[i] == "-f":
            if argv[i+1] == "+":
                make_bg = False
            else:
                make_bg = True
        elif argv[i] == "-w":
            width = argv[i+1]
            resize = True
        elif argv[i] == "-h":
            height = argv[i+1]
            resize = True
        elif argv[i] == "-m":
            resize = True
            resize_with_mean = True

    if make_bg:
        dir_path = path + "neg/"
    else:
        dir_path = path + "pos/"

    if image_type == "png":
        filenames = get_all_png_files(dir_path)
    else:
        filenames = get_all_jpg_files(dir_path)

    if make_bg:
        create_bg_file(path, filenames)
    else:
        create_positive_file(path, filenames)

    if resize:
        if resize_with_mean:
            resize_size = get_mean_size(dir_path, filenames)
            width = resize_size[0]
            height = resize_size[1]

        if (width is 0) or (height is 0):
            print("[!] Error: Given width or height is 0. Aborting...")
            exit(1)

        resize_images(path, dir_path, filenames, (width, height))
