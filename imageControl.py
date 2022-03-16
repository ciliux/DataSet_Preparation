import os

from PIL import Image, ImageTk

def IC_img_annot_path(pathAnnotation, imgName):
    pathAnnot = pathAnnotation + "/" + imgName.split('.')[0] + ".txt"
    return pathAnnot
