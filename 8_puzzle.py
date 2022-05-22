# Atsune Mogi

import random
import tkinter as tk
from PIL import Image, ImageTk

# size of this puzzle
SIZE = 3
# size of images
IMAGE_SIZE = 150
# initialization
B = [[0 for i in range(SIZE)] for j in range(SIZE)]
# set numbers
for i in range(SIZE):
    for j in range(SIZE):
        B[i][j] = (i*SIZE + j + 1) % SIZE**2
# boolian value which means the game is started
GAME = True
# boolian value which means the timer is started
timer_flag = False
# timer digits
minutes, seconds, deciseconds = 0, 0, 0
# the number of times the numbers are moved
cnt_moves = 0
# main window
root = tk.Tk()
# the size of the window
root.geometry(str(IMAGE_SIZE*SIZE+200)+'x'+str(IMAGE_SIZE*SIZE)+'+0+0')
# game title
root.title(str(SIZE**2-1)+' PUZZLE')
# font size
fonts = ('', 40)
# the canvas to draw the images
canvas = tk.Canvas(
    root,
    bg='white',
    width=IMAGE_SIZE*SIZE,
    height=IMAGE_SIZE*SIZE
)
# set the canvas at the coordinates (x, y) = (0, 0)
canvas.place(
    x=0,
    y=0
)
# a label to be displayed as 'Time'
time_label = tk.Label(
    text='Time:',
    font=fonts
)
# place 'Time' label at the coordinates (x, y) = (IMAGE_SIZE*SIZE, 150)
time_label.place(
    x=IMAGE_SIZE*SIZE,
    y=150,
    width=200,
    height=50
)
# a label to be displayed as timer digits
timer_label = tk.Label(
    text='0:00.0',
    font=fonts
)
# place timer digits at the coordinates (x, y) = (IMAGE_SIZE*SIZE, 200)
timer_label.place(
    x=IMAGE_SIZE*SIZE,
    y=200,
    width=200,
    height=50
)
# a label to be displayed as 'Moves'
moves_label = tk.Label(
    text='Moves:',
    font=fonts
)
# place 'Moves' label at the coordinates (x, y) = (IMAGE_SIZE*SIZE), 300)
moves_label.place(
    x=IMAGE_SIZE*SIZE,
    y=300,
    width=200,
    height=50
)
# a label to be displayed as count digits
count_label = tk.Label(
    text='0',
    font=fonts
)
# place count digits at the coordinates (x, y) = (IMAGE_SIZE*SIZE, 350)
count_label.place(
    x=IMAGE_SIZE*SIZE,
    y=350,
    width=200,
    height=50
)

# update timer
def update_timer():
    global minutes, seconds, deciseconds, update_time
    # 0.1 seconds elapses
    deciseconds += 1
    # add 1 to seconds if the number of 0.1 seconds reaches 10
    if deciseconds == 10:
        seconds += 1
        deciseconds = 0
    # add 1 to minutes if the number of seconds reaches 60
    if seconds == 60:
        minutes += 1
        seconds = 0
    # set strings of minutes, seconds, and 0.1 seconds
    minutes_str = str(minutes)
    seconds_str = str(seconds) if seconds > 9 else '0' + str(seconds)
    deciseconds_str = str(deciseconds)
    # set the timer to the current time
    timer_label.config(text=minutes_str + ':' + seconds_str + '.' + deciseconds_str)
    # update the timer every 0.1 seconds
    update_time = timer_label.after(100, update_timer)

# start timer
def start():
    global timer_flag
    # boolean value of the timer true
    timer_flag = True
    # anable to update timer
    update_timer()

# pause timer
def pause():
    global timer_flag
    # boolian value of the timer false
    timer_flag = False
    # disable to update timer
    timer_label.after_cancel(update_time)
    
# reset timer
def reset():
    global timer_flag
    # boolian value of the timer false
    timer_flag = False
    # disable to update timer
    timer_label.after_cancel(update_time)
    # make the timer digits zero
    global minutes, seconds, deciseconds
    minutes, seconds, deciseconds = 0, 0, 0
    timer_label.config(text='0:00.0')

# count the number of times numbers are moved
def count_moves():
    global cnt_moves, count_label
    # add 1 to the number of times numbers are moved
    if timer_flag == True:
        cnt_moves += 1
        count_label.config(text=str(cnt_moves))

# move the tile with the entered number
def move_tile(n):
    # initialization
    a, b, c, d = 0, 0, 0, 0
    # explore where the empty tile is located
    for i in range(SIZE):
        for j in range(SIZE):
            if 0 == B[i][j]:
                a = i
                b = j
    # explore where clicked number is located
    for i in range(SIZE):
        for j in range(SIZE):
            if n == B[i][j]:
                c = i
                d = j
    # move clicked number
    if a == c and b != d:
        if b < d:
            for i in range(d-b):
                B[a][b+i], B[a][b+i+1] = B[a][b+i+1], B[a][b+i]
        else:
            for i in range(b-d):
                B[a][b-i], B[a][b-i-1] = B[a][b-i-1], B[a][b-i]
        # add 1 to the number of the times numbers are moved
        count_moves()
    elif b == d and a != c:
        if a < c:
            for i in range(c-a):
                B[a+i][b], B[a+i+1][b] = B[a+i+1][b], B[a+i][b]
        else:
            for i in range(a-c):
                B[a-i][b], B[a-i-1][b] = B[a-i-1][b], B[a-i][b]
        # add 1 to the number of the times numbers are moved
        count_moves()

# move clicked number
def click_number(event):
    global timer_flag
    # start the timer if timer hasn't started
    if not timer_flag and GAME:
        start()
    # disable click event if the game is cleared
    if not timer_flag and not GAME:
        move_tile(B[SIZE][SIZE]) 
    else:
        # get the coordinates of the mouse pointer.
        x, y = event.x // IMAGE_SIZE, event.y // IMAGE_SIZE
        move_tile(B[y][x])    
        display_images()    
        scan_board()

# display images
def display_images():
    global imgs
    # the list to maintain images
    imgs = []
    # delete all images on the canvas
    canvas.delete('all')
    for i in range(SIZE):
        for j in range(SIZE):
            # open the image with specified number
            img = Image.open('numbers/'+str(B[i][j])+'.png')
            img = ImageTk.PhotoImage(img)
            # append the image to the list
            imgs.append(img)
            # draw the image on the canvas
            img = canvas.create_image(
                j*IMAGE_SIZE,
                i*IMAGE_SIZE,
                image=img,
                anchor=tk.NW
            )

# shuffle the tiles on the board
def shuffle_board():
    # initialization
    a, b, c, d = 0, 0, 0, 0
    cnt = 0
    while cnt < 1000:
        # number to be moved randomly
        n = random.randint(1, SIZE**2 - 1)
        for i in range(SIZE):
            for j in range(SIZE):
                if 0 == B[i][j]:
                    a = i
                    b = j
        for i in range(SIZE):
            for j in range(SIZE):
                if n == B[i][j]:
                    c = i
                    d = j
        # move numbers and add 1 to cnt if the random number is movable
        if a == c or b == d:
            move_tile(n)
            cnt += 1
    
# check the board is cleared
def scan_board():
    global GAME
    # check the each number is placed in collect place
    for i in range(SIZE):
        for j in range(SIZE):
            if B[i][j] != (i*SIZE + j + 1) % SIZE**2:
                break
        else:
            continue
        break
    else:
        GAME = False
    # stop the timer if the game is cleared
    if not GAME and timer_flag:
        pause() 

# shuffle the board when the button is pressed
def shuffle_button():
    # set button to shuffle the board
    button = tk.Button(
        root,
        text='Shuffle',
        font=fonts,
        command=reset_board
    )
    # place 'Shuffle' button at the coordinates (x, y) = (IMAGE_SIZE*SIZE, 0)
    button.place(
        x=IMAGE_SIZE*SIZE,
        y=0,
        width=200,
        height=100
    )

# shuffles the board again
def reset_board():
    global GAME, cnt_moves, count_label
    shuffle_board()
    display_images()
    if not GAME:
        GAME = True
    reset()
    # make the count number 0
    cnt_moves = 0
    count_label.config(text='0')

# main function
def main():
    shuffle_board()
    display_images()
    shuffle_button()
    # enable click
    root.bind('<1>', click_number)
    # keep the window open
    root.mainloop()


if __name__ == '__main__':
    main()