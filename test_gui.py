from tkinter import *
import main
from tkinter import messagebox

# za image rabis from PIL import ImageTk, Image, ampak rabis to se instalirat pip install Pillow

# root widget
root = Tk()
root.title("Hungarian Method")
# ce hoces dodat ikono levo zgoraj
# root.iconbitmap("tam kjer imas to sliko")

################# LABELS ##################
# Creating a Label widget
myLabel1 = Label(root, text="Hungarian Method")
myLabel2 = Label(root, text="Hello World!")
# v Label lahko das:
#   relief = SUNKEN
#   bd = 1
#   anchor = (E,W,N,S) enega od teh, in ga da cisto desno, levo, gor, dol

# Shoving it onto the screen
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=1)
# v grid lahko das columnspan, rowspan, padx, pady
# sticky = W+E stretches



############## BUTTONS ####################
# we need a function for buttons


def myClick():
    myLabel = Label(root, text="I clicked the button")
    myLabel.grid(row=3, column=3)


# Creating a button
myButton = Button(root, text="Click me!", command=myClick)
# nekatere lastnosti:
# state = DISABLED
# padx = 50, pady = 50 changes the size
# command = function, s tem zažene funkcijo ob kliku
# fg = "color" spremeni barvo texta v buttonu
# bg = "color" spremeni barbo buttona
# command = root.quit te vrze ven iz programa 

# da lahko das parameter funkciji rabis dati comman= lambda: myClick()

# putting on screen
myButton.grid(row=2, column=2)

############ INPUT DATA #############
# creating an entry
e = Entry(root)
# putting it on screen
e.grid(row=4, column=4)
# lastnosti:
# width, spremeni velikost
# fg, bg
# borderwidth
# lahko namesto grid das grid_forget() in bo izbrisal to zadevo

# e.get() dobi ta text ki ga napises
# inster da text v entry
e.insert(0, "Enter your name: ")

# da deletas kar je z v notr das e.delete(0, END)


def Name():
    txt = e.get()
    L = Label(root, text=txt)
    L.grid(row=6, column=4)


B = Button(root, text="Enter your name", command=Name)
B.grid(row=5, column=4)


############ IMAGES #############
# my_img = ImageTk.PhotoImage(Image.open("pot do slike"))
# da das sliko na screen rabis se en widget:
# photoLabel = Label(image=my_img)
# photoLabel.pack()


########### FRAMES ##############
frame = LabelFrame(root, text="This is a frame")
frame.grid(row=6, column=6)
b = Button(frame, text="Don't click", command=Name)
b.grid(row=0, column=0)


############# ce hoces neki uporabit zunaj funkcije dodas global, torej global variable_name

############# MESSAGE BOX ############
def popup():
    # showinfo, showwarning, showerror, askquestion, askokcancel, askyesno
    response = messagebox.askyesno("this is my popup", "Hello world")
    Label(root, text=response).grid(row=8,column=7)

Button(root, text="Popup", command=popup).grid(row=7,column=7)


########## CREATE NEW WINDOW ###############
def openwindow():
    top = Toplevel()
    top.geometry("650x250")
    top.title("Second Window")
    lb = Label(top, text="Hello World!")
    lb.pack()
    # for images you need them to be global variables
    # to close you do a button with command=top.destroy


btn = Button(root, text="Open Second Window", command=openwindow)
btn.grid(row=9,column=9)




# main loop
root.mainloop()