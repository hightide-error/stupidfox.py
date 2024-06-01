import random
import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import os

cwd = os.getcwd()
print(cwd)

#starting positions
x = 1400
y = 900

#various speed parameters
event_time = 10
update_time = 20
x_move = 5
y_move = 3

#image
impath = cwd + "/tsukasa_walk.gif"
explodepath = cwd + "/explosion.gif"
imX = 212
imY = 219

cycle = 0
check = 1
walk_left = [1, 2]
walk_leftup = [3, 4]
walk_leftdown = [5, 6]
walk_right = [7, 8]
walk_rightup = [9, 10]
walk_rightdown = [11, 12]
event_number = random.randrange(1,12,1)

explodeBool = False
explodeReady = False

window = tk.Tk()

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

#transfer random no. to event
def event(cycle, check, event_number, x, y):
    #first check if we're in bounds or not, may set the event based on that
    if (x < 0) or (y < 0) or (x > screenWidth - imX) or (y > screenHeight - imY):
        if x < 0:
            if check == 0:
                check = 3
                print('bounce, walkright')
                window.after(event_time, update, cycle, check, event_number, x, y)
            elif check == 1:
                check = 5
                print('bounce, walkrightdown')
                window.after(event_time, update, cycle, check, event_number, x, y)
            else:
                check = 4
                print('bounce, walkrightup')
                window.after(event_time, update, cycle, check, event_number, x, y)
        elif y < 0:
            if check == 1:
                check = 2
                print('bounce, walkleftdown')
                window.after(event_time, update, cycle, check, event_number, x, y)
            else:
                check = 5
                print('bounce, walkrightdown')
                window.after(event_time, update, cycle, check, event_number, x, y)
        elif x > screenWidth - imX:
            if check == 3:
                check = 0
                print('bounce, walkleft')
                window.after(event_time, update, cycle, check, event_number, x, y)
            elif check == 2:
                check = 5
                print('bounce, walkleftdown')
                window.after(event_time, update, cycle, check, event_number, x, y)
            else:
                check = 1
                print('bounce, walkleftup')
                window.after(event_time, update, cycle, check, event_number, x, y)
        elif y > screenHeight - imY:
            if check == 2:
                check = 1
                print('bounce, walkleftup')
                window.after(event_time, update, cycle, check, event_number, x, y)
            else:
                check = 4
                print('bounce, walkrightup')
                window.after(event_time, update, cycle, check, event_number, x, y)
        event_number = (check+1)*2    


    else:
        if event_number in walk_left:
            check = 0
            print('walkleft')
            window.after(event_time, update, cycle, check, event_number, x, y)
        elif event_number in walk_leftup:
            check = 1
            print('walkleftup')
            window.after(event_time, update, cycle, check, event_number, x, y)
        elif event_number in walk_leftdown:
            check = 2
            print('walkleftdown')
            window.after(event_time, update, cycle, check, event_number, x, y)
        elif event_number in walk_right:
            check = 3
            print('walkright')
            window.after(event_time, update, cycle, check, event_number, x, y)
        elif event_number in walk_rightup:
            check = 4
            print('walkrightup')
            window.after(event_time, update, cycle, check, event_number, x, y)
        else:
            check = 5
            print('walkrightdown')
            window.after(event_time, update, cycle, check, event_number, x, y)

def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) -1:
        cycle+=1
    elif event_number == 99:
        window.destroy()
        exit()
    else:
        cycle = 0
        if explodeBool == True:
            global explodeReady
            explodeReady = True
        #smoother way of going between states
        event_number += random.randrange(-6, 7, 1)
        if event_number < 1:
            event_number += 12
        if event_number > 12:
            event_number -= 12
    return cycle, event_number


def update(cycle, check, event_number, x, y):
    if explodeReady == True:
        print("explode")
        frame = explode[cycle]
        event_number = 99
        cycle, event_number = gif_work(cycle, explode, event_number, 1, 12)
    elif check == 0: #walk toward left
        frame = walkLeft[cycle]
        cycle, event_number = gif_work(cycle, walkLeft, event_number, 1, 12)
        x -= x_move
    elif check == 1: #walk toward left and up
        frame = walkLeft[cycle]
        cycle, event_number = gif_work(cycle, walkLeft, event_number, 1, 12)
        x -= x_move
        y -= y_move
    elif check == 2: #walk toward left and down
        frame = walkLeft[cycle]
        cycle, event_number = gif_work(cycle, walkLeft, event_number, 1, 12)
        x -= x_move
        y += y_move
    elif check == 3: #walk toward right
        frame = walkRight[cycle]
        cycle, event_number = gif_work(cycle, walkRight, event_number, 1, 12)
        x += x_move
    elif check == 4: #walk toward right and up
        frame = walkRight[cycle]
        cycle, event_number = gif_work(cycle, walkRight, event_number, 1, 12)
        x += x_move
        y -= y_move
    elif check == 5: #walk toward right and down
        frame = walkRight[cycle]
        cycle, event_number = gif_work(cycle, walkRight, event_number, 1, 12)
        x += x_move
        y += y_move
    window.geometry(str(imX)+'x'+str(imY)+'+'+str(x)+'+'+str(y))
    label.configure(image=frame)
    window.after(update_time, event, cycle, check, event_number, x, y)

def callback(event):
    print("clicked at x=" + str(event.x) + ", y=" + str(event.y))
    global explodeBool
    explodeBool = True
    
        
#putting tsukasa's walk animation into left and right arrays
walkLeft = [tk.PhotoImage(file=impath, format = 'gif -index %i' %(i)) for i in range(46)]
walkRight = []
walkRightIm = Image.open(impath)
for gifFrame in range(0, walkRightIm.n_frames):
    walkRightIm.seek(gifFrame)
    thisFrame = walkRightIm.transpose(Image.FLIP_LEFT_RIGHT)
    walkRight.append(ImageTk.PhotoImage(thisFrame))

#putting the explosion gif into an array, but in the right order because it's not by default
explodeIm = Image.open(explodepath)
explode = []
f = 9
for gifFrame in range(0, explodeIm.n_frames):
    explodeIm.seek(f)
    f += 1
    if f > 16:
        f = 0
    explode.append(ImageTk.PhotoImage(explodeIm))

window.overrideredirect(True)
window.wait_visibility(window)
window.wm_attributes("-alpha", 0.5)

window.bind("<Button-1>", callback)

label = tk.Label(window, bd=0)
label.pack()

#loop the program
window.after(100, update, cycle, check, event_number, x, y)

window.mainloop()
    

