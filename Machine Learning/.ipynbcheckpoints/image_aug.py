import cv2
import os
# from skimage.exposure import rescale_intensity
# from skimage.segmentation import slic
# from skimage.util import img_as_float
# from skimage import io
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder", type=str, help="folder name")
parser.add_argument("-i", "--index", type=int, help="index")
args = parser.parse_args()

#co-relation between Opencv and Pillow Image Rectangle box
# (x1, y1) (left, top)
# (right, bottom) (x2, y2)

# (top,right,bottom,left)
# (32,64,0,0)

Folder_name=args.folder
Extension=".jpg"
index = args.index

#RESIZE
def resize_image(image,w,h):
    image=cv2.resize(image,(w,h))
    cv2.imwrite(Folder_name+"/Resize-"+str(w)+"*"+str(h)+Extension, image)

#crop
def crop_image(image,y1,y2,x1,x2):
    image=image[y1:y2,x1:x2]
    cv2.imwrite(Folder_name+"/Crop-"+str(x1)+str(x2)+"*"+str(y1)+str(y2)+Extension, image)

def padding_image(image,topBorder,bottomBorder,leftBorder,rightBorder,color_of_border=[0,0,0]):
    image = cv2.copyMakeBorder(image,topBorder,bottomBorder,leftBorder,
        rightBorder,cv2.BORDER_CONSTANT,value=color_of_border)
    cv2.imwrite(Folder_name + "/padd-" + str(topBorder) + str(bottomBorder) + "*" + str(leftBorder) + str(rightBorder) + Extension, image)

def flip_image(image,dir):
    image = cv2.flip(image, dir)
    cv2.imwrite(Folder_name + "/flip-" + str(dir)+Extension, image)

def invert_image(image,channel):
    # image=cv2.bitwise_not(image)
    image=(channel-image)
    cv2.imwrite(Folder_name + "/aug/invert-"+str(channel)+"-"+str(index)+Extension, image)

def add_light(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    image=cv2.LUT(image, table)
    if gamma>=1:
        cv2.imwrite(Folder_name + "/aug/light-"+str(gamma)+"-"+str(index)+Extension, image)
    else:
        cv2.imwrite(Folder_name + "/dark-" + str(gamma) + Extension, image)

def add_light_color(image, color, gamma=1.0):
    invGamma = 1.0 / gamma
    image = (color - image)
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    image=cv2.LUT(image, table)
    if gamma>=1:
        cv2.imwrite(Folder_name + "/aug/light_color-"+str(gamma)+"-"+str(index)+Extension, image)
    else:
        cv2.imwrite(Folder_name + "/dark_color" + str(gamma) + Extension, image)

def saturation_image(image,saturation):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    v = image[:, :, 2]
    v = np.where(v <= 255 - saturation, v + saturation, 255)
    image[:, :, 2] = v

    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    cv2.imwrite(Folder_name + "/saturation-" + str(saturation) + Extension, image)

def hue_image(image,saturation):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    v = image[:, :, 2]
    v = np.where(v <= 255 + saturation, v - saturation, 255)
    image[:, :, 2] = v

    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    cv2.imwrite(Folder_name + "/aug/hue-" + str(saturation) +"-"+ str(index) + Extension, image)


for filename in os.listdir(args.folder):
    f = os.path.join(args.folder, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # print(f)
        image=cv2.imread(f)
        hue_image(image, 100)
        add_light(image,4.0)
        # invert_image(image,150)
        invert_image(image,100)
        # saturation_image(image,200)
        index += 1


# resize_image(image,450,400)

# crop_image(image,100,400,0,350)#(y1,y2,x1,x2)(bottom,top,left,right)
# crop_image(image,100,400,100,450)#(y1,y2,x1,x2)(bottom,top,left,right)
# crop_image(image,0,300,0,350)#(y1,y2,x1,x2)(bottom,top,left,right)
# crop_image(image,0,300,100,450)#(y1,y2,x1,x2)(bottom,top,left,right)
# crop_image(image,100,300,100,350)#(y1,y2,x1,x2)(bottom,top,left,right)

# padding_image(image,100,0,0,0)#(y1,y2,x1,x2)(bottom,top,left,right)
# padding_image(image,0,100,0,0)#(y1,y2,x1,x2)(bottom,top,left,right)
# padding_image(image,0,0,100,0)#(y1,y2,x1,x2)(bottom,top,left,right)
# padding_image(image,0,0,0,100)#(y1,y2,x1,x2)(bottom,top,left,right)
# padding_image(image,100,100,100,100)#(y1,y2,x1,x2)(bottom,top,left,right)

# flip_image(image,0)#horizontal
# flip_image(image,1)#vertical
# flip_image(image,-1)#both

# superpixel_image(image_file,100)
# superpixel_image(image_file,50)
# superpixel_image(image_file,25)
# superpixel_image(image_file,75)
# superpixel_image(image_file,200)

# invert_image(image,255)
# invert_image(image,200)
# invert_image(image,150)
# invert_image(image,100)
# invert_image(image,50)

# add_light(image,1.5)
# add_light(image,2.0)
# add_light(image,2.5)
# add_light(image,3.0)
# add_light(image,4.0)
# add_light(image,5.0)
# add_light(image,0.7)
# add_light(image,0.4)
# add_light(image,0.3)
# add_light(image,0.1)

# add_light_color(image,255,1.5)
# add_light_color(image,200,2.0)
# add_light_color(image,150,2.5)
# add_light_color(image,100,3.0)
# add_light_color(image,50,4.0)
# add_light_color(image,255,0.7)
# add_light_color(image,150,0.3)
# add_light_color(image,100,0.1)

# saturation_image(image,50)
# saturation_image(image,100)
# saturation_image(image,150)
# saturation_image(image,200)

# hue_image(image,50)
# hue_image(image,100)
# hue_image(image,150)
# hue_image(image,200)
