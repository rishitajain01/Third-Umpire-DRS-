import time
import tkinter
import cv2
import time
import PIL.Image,PIL.ImageTk # python image library
from functools import partial
import threading
import imutils

stream = cv2.VideoCapture("clip.mp4")

flag=True

def play(speed):
    global flag
    print(f"You clicked on play. speed is {speed}")
    frame1=stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1+speed)

    grabbed,frame = stream.read()
    if not grabbed:
        canvas.create_text(234, 226, fill="red", font="Times 40 bold", text="clip over")
    else:
        frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
        if flag:
            canvas.create_text(134, 26, fill="black", font="Times 26 bold", text="Decision Pending")
        flag = not flag


def pending(decision):
    # 1)Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    # 2) Wait for 2 sec
    time.sleep(2)
    # 3)Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    # 4)wait 2 sec
    time.sleep(2)

    # display the decision
    if decision == "out":
        decisionimg = "out.png"
    else:
        decisionimg = "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionimg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


def out():
    thread=threading.Thread(target=pending , args=("out",))
    thread.daemon = 1
    thread.start()
    print("player is out")
def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("player is not out")

# main window width and height
SET_WIDTH = 650
SET_HEIGHT = 400

# tkinter gui
window = tkinter.Tk()
window.title("Warriors Third Umpire")
cv_img = cv2.cvtColor(cv2.imread("welcome.jpg"),cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width= SET_WIDTH, height = SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
canvas.image = photo
image_on_canvas = canvas.create_image(0,0,anchor=tkinter.NW,image=photo)
canvas.pack()

btn = tkinter.Button(window,text = "<< Previous(fast)",bg="#4dd2ff",width=20,command = partial(play,-25))
btn.pack()

btn = tkinter.Button(window,text = "<< Previous(slow)",bg="#4dd2ff",width=20,command = partial(play,-5))
btn.pack()

btn = tkinter.Button(window,text = "Next(fast) >>",bg="#4dd2ff",width=20,command = partial(play,25))
btn.pack()

btn = tkinter.Button(window,text = "Next (slow) >>",bg="#4dd2ff",width=20,command = partial(play,5))
btn.pack()

btn = tkinter.Button(window,text = "NOT OUT",bg="#4dd2ff",width=20, command=not_out)
btn.pack()

btn = tkinter.Button(window,text = "OUT",bg="#4dd2ff",width=20,command=out)
btn.pack()
window.mainloop()