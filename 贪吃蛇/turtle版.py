from turtle import *
from random import randrange


def square(x, y, size, color_name):
    up()
    goto(x, y)
    color(color_name)
    begin_fill()

    forward(size)
    left(90)
    forward(size)
    left(90)
    forward(size)
    left(90)
    forward(size)
    left(90)
    end_fill()


snack = [[0, 0], [10, 0], [20, 0], [30, 0]]
apple_x = randrange(-20, 20) * 10
apple_y = randrange(-20, 20) * 10
aim_x = 0
aim_y = 10


def change(x, y):
    global aim_x, aim_y
    aim_x = x
    aim_y = y


def inside():
    if -210 <= snack[-1][0] <= 200 and -210 <= snack[-1][1] < 210:
        return True
    else:
        return False


def gameLoop():
    global apple_x, apple_y
    clear()
    snack.append([snack[-1][0] + aim_x, snack[-1][1] + aim_y])
    if not inside():
        return
    if snack[-1][0] != apple_x or snack[-1][1] != apple_y:
        snack.pop(0)
    else:
        apple_x = randrange(-20, 20) * 10
        apple_y = randrange(-20, 20) * 10
    for n in range(len(snack)):
        square(snack[n][0], snack[n][1], 10, "black")
    square(apple_x, apple_y, 10, "red")
    ontimer(gameLoop, 200)
    update()


setup(420, 420, 0, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(0, 10), "w")
onkey(lambda: change(0, -10), "s")
onkey(lambda: change(10, 0), "d")
onkey(lambda: change(-10, 0), "a")
gameLoop()
done()
