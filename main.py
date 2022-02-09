import os
import tkinter
import tkinter.filedialog
from tkinter import*
from PIL import Image, ImageTk

from imageControl import *

obj = Tk()

obj.title("Dataset preparation")
obj.geometry("1000x700")

allClasses = []
global colors
colors = ["#FF2400", "#5CFF00", "#00DBFF", "#FF00FF", "#FF7F00", "#D4E01F", "#FF9500"]

#TODO divide code into smaller functions and through classes
def newP():
    print("New")
    global newProj
    newProj= Tk()
    newProj.title("New project")
    newProj.geometry("250x230")
    pNameLabel = Label(newProj, text='Project name')
    pNameLabel.place(x=5, y=5)
    global nameBox
    nameBox = Text(newProj, height=1, width=20)
    nameBox.place(x=5, y=30)
    global dirLabel
    dirLabel = Label(newProj, text='label')
    dirLabel.place(x=100, y=60)
    selectDir = Button(newProj, text='Select location', command=directory)
    selectDir.place(x=5, y=55)
    #TODO: add checkbox for object detection/segmentation
    createButton = Button(newProj, text='Create', command=createP)
    createButton.place(x=200, y=200)
    return

def directory():
    dirLabel.config(text=tkinter.filedialog.askdirectory())
    return

def openP():
    print("Open")
    projDir = tkinter.filedialog.askdirectory()
    print(projDir)
    return

def saveP():
    print("Save")
    return

def createP():
    global mainFile, path, pathAnnotation, pathImg
    path = dirLabel.cget("text") + "/" + nameBox.get("1.0", "end-1c")
    pathAnnotation = path + "/Annotation"
    pathImg = path + "/Images"
    os.mkdir(path)
    os.mkdir(pathAnnotation)
    os.mkdir(pathImg)
    newProj.destroy()
    return

'''def Classes():
    cW = Tk()
    cW.title("Classes")
    cW.geometry("200x300")
    global classList
    classList = Listbox(cW, height=10, selectmode='browse')
    classList.grid(column=0, row=0, sticky='nwes')
    classList.place(x=5, y=2)
    for cl in allClasses:
        classList.insert(END, cl)
    global cText
    cText = Text(cW, height=1, width=20)
    cText.place(x=5, y=180)
    #addClassButton = Button(cW, text='Add', command=add_Class)
    addClassButton.place(x=5, y=200)
    #delClassButton = Button(cW, text='Delete', command=del_Class)
    delClassButton.place(x=50, y=200)
    return'''

def image_open(index):

    return

def image_selected(event):
    index = imageList.index(ANCHOR)
    file = open(path + "/info.txt", 'r')
    images = file.readlines()
    img = ImageTk.PhotoImage(Image.open(pathImg + "/" + images[index].removesuffix("\n")))

    canvas.photo = img
    canvas.create_image(0, 0, image=img, anchor='nw')
    #objectList.delete(0, END)
    name = imageList.get(ANCHOR).split('.')
    imgAnnotationPath = pathAnnotation + "/" + name[0] + ".txt"
    if os.path.isfile(imgAnnotationPath):
        display_anotation(imgAnnotationPath)
    return

def display_anotation(imgAnnotationPath):
    imgAnnotation = open(imgAnnotationPath, 'r')
    anotationData = imgAnnotation.readlines()
    for anData in anotationData:
        annot = anData.split(';')
        draw_rect1(annot[0], annot[1], annot[2], annot[3], annot[4])
    return

def get_image_dir():
    types = (("jpg files", "*.jpg"), ("png files", "*.png"))
    fnames = tkinter.filedialog.askopenfilenames(title='Open an image', initialdir='C://', filetypes=types)
    add_images(fnames)
    return

def add_images(fnames):
    mainFile = open(path + "/info.txt", 'a')
    for file in fnames:
        img = Image.open(file)
        parts = file.split('/')
        file = parts[len(parts) - 1]
        imageList.insert(END, file)
        img.save(pathImg + "/" + file)
        mainFile.write(file + '\n')
    mainFile.close()
    return

def draw_rect(event):
    if str(event.type) == '4':
        canvas.old_coords = event.x, event.y

    elif str(event.type) == '5':
        x, y = event.x, event.y
        x1, y1 = canvas.old_coords
        #canvas.create_rectangle((x1, y1, x, y), fill='', outline='red')
        draw_rect1(objClass, x1, y1, x, y)
        add_Obj(x1, y1, x, y)
        print(x1, y1, x, y)

def draw_rect1(classOfObj, x1, y1, x, y):
    canvas.create_rectangle((x1, y1, x, y), fill='', outline=colors[allClasses.index(classOfObj)])
    return

def add_Obj(x1, y1, x, y): #TODO show all object count in a image, next to the name in image list
    '''global newObjWind, classes, objClass TODO: add image info field with count of objects in different classes
    newObjWind = Tk()
    newObjWind.title("New object")
    newObjWind.geometry("200x200")
    classes = Listbox(newObjWind, height=10, selectmode='browse')
    classes.bind("<<ListboxSelect>>", class_select)
    for cl in allClasses:
        classes.insert(END, cl)
    classes.grid(column=0, row=0, sticky='nwes')
    classes.place(x=5, y=2)
    global objSaveText'''
    objSaveText = "{0};{1};{2};{3};".format(x1, y1, x, y)
    name = imageList.get(ANCHOR).split('.')
    imgAnnotation = open(pathAnnotation + "/" + name[0] + ".txt", 'a')
    text = objClass + ";" + objSaveText + "\n"
    imgAnnotation.write(text)
    imgAnnotation.close()
    return

def class_select(event): #TODO: different class objects in different colors
    global objClass
    objClass = classList.get(ANCHOR)
    '''name = imageList.get(ANCHOR).split('.')
    imgAnnotation = open(pathAnnotation + "/" + name[0] + ".txt", 'a')
    text = objClass + ";" + objSaveText + "\n"
    imgAnnotation.write(text)
    imgAnnotation.close()
    classList.insert(END, objClass)
    newObjWind.destroy()'''
    return

def add_Class():
    name = cText.get("1.0", "end-1c")
    classList.insert(END, name)
    cText.delete("1.0", "end-1c")
    allClasses.append(classList.get(END))
    classLFile = open(path + "/classes.txt", 'a')
    classLFile.write(name + "\n")
    classLFile.close()
    return

def del_Class():
    allClasses.remove(classList.get(ANCHOR))
    classList.delete(ANCHOR)
    classLFile = open(path + "/classes.txt", 'w')
    for cl in allClasses:
        classLFile.write(cl + "\n")
    classLFile.close()
    return

mb = Menubutton(obj, text="Project", background='gray')
mb.grid()
mb.menu = Menu(mb, tearoff=0)
mb["menu"] = mb.menu

#classButton = Button(obj, text='Classes', command=Classes)
#classButton.place(x=75, y=580)

mb.menu.add_command(label="New", command=newP)
mb.menu.add_command(label="Open", command=openP)
mb.menu.add_command(label="Save", command=saveP)
mb.place(x=5, y=2)

imgLabel = Label(obj, text='Images')
imgLabel.place(x=5, y=30)
allImages = ()
imageVar = StringVar(value=allImages) #TODO: fix list not showing selected item after clicking elsewhere
imageList = Listbox(obj, listvariable=imageVar, height=7, selectmode='browse')
imageList.grid(column=0, row=0, sticky='nwes')
imageList.place(x=5, y=50)
imageList.bind("<<ListboxSelect>>", image_selected)

canvas = Canvas(obj, width=500, height=500)
canvas.old_coords = None
canvas.bind('<ButtonPress-1>', draw_rect)
canvas.bind('<ButtonRelease-1>', draw_rect)
canvas.pack()

button = Button(obj, text='Add', command=get_image_dir)
button.place(x=5, y=180)

objLabel = Label(obj, text='Objects')
objLabel.place(x=5, y=230)

allObj = ()
objVar = StringVar(value=allObj)
classList = Listbox(obj, listvariable=objVar, height=20, selectmode='browse')
classList.bind("<<ListboxSelect>>", class_select)
classList.place(x=5, y=250)

addClassButton = Button(obj, text='Add', command=add_Class)
addClassButton.place(x=5, y=600)
delClassButton = Button(obj, text='Delete', command=del_Class)
delClassButton.place(x=85, y=600)
cText = Text(obj, height=1, width=10)
cText.place(x=5, y=580)

obj.mainloop()





