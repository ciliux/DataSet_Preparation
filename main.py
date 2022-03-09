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
global colors, highLightColor
colors = ["#FF2400", "#5CFF00", "#00DBFF", "#FF00FF", "#FF7F00", "#D4E01F", "#FF9500"]
highLightColor = ["#ff0000", "#77ff00", "#fb00ff", "#ff0000"]

#TODO divide code into smaller functions and through classes
def newP():
    print("New")
    clear_GUI()
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


def openP():
    print("Open")
    clear_GUI()
    global path
    path = tkinter.filedialog.askdirectory()
    print(path)
    create_paths()
    load_classes()
    load_images(path)
    return

def saveP():
    print("Save")
    return

def clear_GUI():
    imageList.delete("0", END)
    classList.delete("0", END)
    canvas.delete("all")
    infoCList.delete("0", END)
    infoObjList.delete("0", END)
    allClasses.clear()
    return

def directory():
    dirLabel.config(text=tkinter.filedialog.askdirectory())
    return

def create_paths():
    global pathAnnotation, pathImg
    pathAnnotation = path + "/Annotation"
    pathImg = path + "/Images"
    return

def createP():
    global mainFile, path
    path = dirLabel.cget("text") + "/" + nameBox.get("1.0", "end-1c")
    create_paths()
    os.mkdir(path)
    os.mkdir(pathAnnotation)
    os.mkdir(pathImg)
    newProj.destroy()
    return

def get_img_annot_path():
    name = imageList.get(ANCHOR).split('.')
    pathAnnot = pathAnnotation + "/" + name[0] + ".txt"
    return pathAnnot

def image_selected(event):
    index = imageList.index(ANCHOR)
    image_open(index)
    imgAnnotationPath = get_img_annot_path()
    if os.path.isfile(imgAnnotationPath):
        display_anotation(imgAnnotationPath)
        load_img_info(imgAnnotationPath)
    return

def image_open(index):
    file = open(path + "/info.txt", 'r')
    images = file.readlines()
    file.close()
    global img
    img = ImageTk.PhotoImage(Image.open(pathImg + "/" + images[index].removesuffix("\n")))
    canvas.photo = img
    canvas.create_image(0, 0, image=img, anchor='nw')
    return

def read_img_annot(imgAnnotationPath):
    imgAnnotation = open(imgAnnotationPath, 'r')
    annotationData = imgAnnotation.readlines()
    imgAnnotation.close()
    return annotationData

def load_img_info(imgAnnotationPath):
    countOfObj = [0] * 20
    annotationData = read_img_annot(imgAnnotationPath)
    for anData in annotationData:
        annot = anData.split(';')
        countOfObj[allClasses.index(annot[0])] += 1

    infoCList.delete('0', END)
    for i in range(len(allClasses)):
        infoCList.insert(END, allClasses[i] + "  " + str(countOfObj[i]))
    return

def load_obj_info(event):
    imgAnnotationPath = get_img_annot_path()
    selectedClass = infoCList.get(ANCHOR)
    annotData = read_img_annot(imgAnnotationPath)
    infoObjList.delete('0', END)
    for anData in annotData:
        annot = anData.split(';', maxsplit=1)
        if annot[0]==selectedClass.split(' ')[0]:
            infoObjList.insert(END, annot[1].rstrip('\n'))
    return

def highlight_selected_obj(event):
    reset_canvas()
    coords = infoObjList.get(ANCHOR).split(';')
    draw_rect1(highLightColor[0], coords[0], coords[1], coords[2], coords[3])
    draw_rect1(highLightColor[1], int(coords[0])+1, int(coords[1])+1, int(coords[2])-1, int(coords[3])-1)
    return

def reset_canvas():
    canvas.delete("all")
    canvas.photo = img
    canvas.create_image(0, 0, image=img, anchor='nw')
    display_anotation(get_img_annot_path())
    return

def del_Object():
    imgAnnotPath = get_img_annot_path()
    annotationData = read_img_annot(imgAnnotPath)
    writer = open(imgAnnotPath, 'w')
    objToDelete = infoCList.get(ANCHOR).split(' ')[0] + ";" + infoObjList.get(ANCHOR) + "\n"
    print(annotationData)
    for anData in annotationData:
        if anData != objToDelete:
            writer.write(anData)
    writer.close()
    reset_canvas()
    load_img_info(imgAnnotPath)
    return

def display_anotation(imgAnnotationPath):
    annotationData = read_img_annot(imgAnnotationPath)
    for anData in annotationData:
        annot = anData.split(';')
        draw_rect1(colors[allClasses.index(annot[0])], annot[1], annot[2], annot[3], annot[4])
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
        imgListText = "{:<25}".format(file) + "0"
        imageList.insert(END, imgListText)

        img.save(pathImg + "/" + file)
        mainFile.write(file + '\n')
    mainFile.close()
    return

def load_images(path):
    imgFile = open(path + "/info.txt", 'r')
    fnames = imgFile.readlines()
    for file in fnames:
        count = '0'
        imgAnnotPath = pathAnnotation + '/' + file.split('.')[0] + '.txt'
        if os.path.exists(imgAnnotPath):
            annotData = read_img_annot(imgAnnotPath)
            count = str(len(annotData))
        imgListText = "{:<25}".format(file) + count
        imageList.insert(END, imgListText)
    imgFile.close()
    return

def draw_rect(event):
    if str(event.type) == '4': #and imageList.curselection():
        canvas.old_coords = event.x, event.y

    elif str(event.type) == '5':# and imageList.curselection():
        x, y = event.x, event.y
        x1, y1 = canvas.old_coords
        draw_rect1(colors[allClasses.index(objClass)], x1, y1, x, y)
        add_Obj(x1, y1, x, y)
        print(x1, y1, x, y)

def draw_rect1(color, x1, y1, x, y):
    canvas.create_rectangle((x1, y1, x, y), fill='', outline=color)
    return

def add_Obj(x1, y1, x, y):
    objSaveText = "{0};{1};{2};{3};".format(x1, y1, x, y)
    text = objClass + ";" + objSaveText + "\n"

    name = imageList.get(ANCHOR).split('.')
    imgAnnotation = open(pathAnnotation + "/" + name[0] + ".txt", 'a')
    imgAnnotation.write(text)
    imgAnnotation.close()
    update_Obj_Count()
    load_img_info(get_img_annot_path())
    return

def update_Obj_Count():
    text = imageList.get(ANCHOR).strip()
    number = text[len(text) - 3:len(text)].strip()
    text = text.rstrip(number)
    number = int(number)
    number += 1
    text = text + str(number)
    index = imageList.index(ANCHOR)
    imageList.insert(index + 1, text)
    imageList.delete(index)
    return

def class_select(event):
    global objClass
    objClass = classList.get(ANCHOR)
    return

def add_Class():
    name = cText.get("1.0", "end-1c")
    classList.insert(END, name)
    cText.delete("1.0", "end-1c")
    allClasses.append(classList.get(END))
    append_class_file(name)
    return

def load_classes():
    classFile = open(path + "/classes.txt", 'r')
    classNames = classFile.readlines()
    for name in classNames:
        name = name.removesuffix('\n')
        classList.insert(END, name)
        allClasses.append(name)#classList.get(END))
    return

def append_class_file(name):
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

mb.menu.add_command(label="New", command=newP)
mb.menu.add_command(label="Open", command=openP)
#mb.menu.add_command(label="Save", command=saveP)
mb.place(x=5, y=2)

imgLabel = Label(obj, text='Images')
imgLabel.place(x=5, y=30)
allImages = ()
imageVar = StringVar(value=allImages)
imageList = Listbox(obj, listvariable=imageVar, height=7, selectmode='browse', exportselection=False)
imageList.grid(column=0, row=0, sticky='nwes')
imageList.place(x=5, y=50)
imageList.bind("<<ListboxSelect>>", image_selected)

infoCList = Listbox(obj, height=7, selectmode='browse', exportselection=False)
infoCList.place(x=140, y=250)
infoCList.bind("<<ListboxSelect>>", load_obj_info)

infoObjList = Listbox(obj, height=7, selectmode='browse', exportselection=False)
infoObjList.place(x=140, y=380)
infoObjList.bind("<<ListboxSelect>>", highlight_selected_obj)

delObjButton = Button(obj, text="Delete object", command=del_Object)
delObjButton.place(x=140, y=500)

canvas = Canvas(obj, width=500, height=500)
canvas.old_coords = None
canvas.bind('<ButtonPress-1>', draw_rect)
canvas.bind('<ButtonRelease-1>', draw_rect)
canvas.place(x=300, y=10)

button = Button(obj, text='Add', command=get_image_dir)
button.place(x=5, y=180)

objLabel = Label(obj, text='Objects')
objLabel.place(x=5, y=230)

allObj = ()
objVar = StringVar(value=allObj)
classList = Listbox(obj, listvariable=objVar, height=20, selectmode='browse', exportselection=False)
classList.bind("<<ListboxSelect>>", class_select)
classList.place(x=5, y=250)

addClassButton = Button(obj, text='Add', command=add_Class)
addClassButton.place(x=5, y=600)
delClassButton = Button(obj, text='Delete', command=del_Class)
delClassButton.place(x=85, y=600)
cText = Text(obj, height=1, width=10)
cText.place(x=5, y=580)

obj.mainloop()





