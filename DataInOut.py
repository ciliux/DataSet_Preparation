def FR_read_img_annot(imgAnnotationPath):
    imgAnnotation = open(imgAnnotationPath, 'r')
    annotationData = imgAnnotation.readlines()
    imgAnnotation.close()
    return annotationData

def FR_read_info(path):
    file = open(path + "/info.txt", 'r')
    images = file.readlines()
    file.close()
    return images

def FR_read_classes(path):
    classFile = open(path + "/classes.txt", 'r')
    classNames = classFile.readlines()
    classFile.close()
    return classNames

def FA_annotation(pathAnnotation, fname, text):
    #name = imageList.get(ANCHOR).split('.')
    imgAnnotation = open(pathAnnotation + "/" + fname + ".txt", 'a')
    imgAnnotation.write(text)
    imgAnnotation.close()
    return

def FA_class(path, cName):
    classLFile = open(path + "/classes.txt", 'a')
    classLFile.write(cName + "\n")
    classLFile.close()
    return

def FW_class(path, allClasses):
    classLFile = open(path + "/classes.txt", 'w')
    for cl in allClasses:
        classLFile.write(cl + "\n")
    classLFile.close()
    return

def FW_annotation(path, annotationData):
    writer = open(path, 'w')
    for anData in annotationData:
        writer.write(anData)
    writer.close()
    return
