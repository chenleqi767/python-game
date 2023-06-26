import turtle
import random


class Block:
    def __init__(self, color, tiles):
        self.color = color
        self.tiles = tiles


I = Block("cyan", [[[1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0]],

                   [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [1, 1, 1, 1]]])

J = Block("blue", [[[0, 1, 0],
                    [0, 1, 0],
                    [1, 1, 0]],

                   [[0, 0, 0],
                    [1, 1, 1],
                    [0, 0, 1]],

                   [[1, 1, 0],
                    [1, 0, 0],
                    [1, 0, 0]],

                   [[0, 0, 0],
                    [1, 0, 0],
                    [1, 1, 1]]])

L = Block("orange", [[[1, 0, 0],
                      [1, 0, 0],
                      [1, 1, 0]],

                     [[0, 0, 0],
                      [0, 0, 1],
                      [1, 1, 1]],

                     [[0, 1, 1],
                      [0, 0, 1],
                      [0, 0, 1]],

                     [[0, 0, 0],
                      [1, 1, 1],
                      [1, 0, 0]]])

S = Block("lime", [[[0, 0, 0],
                    [0, 1, 1],
                    [1, 1, 0]],

                   [[1, 0, 0],
                    [1, 1, 0],
                    [0, 1, 0]]])

Z = Block("red", [[[0, 0, 0],
                   [1, 1, 0],
                   [0, 1, 1]],

                  [[0, 1, 0],
                   [1, 1, 0],
                   [1, 0, 0]]])

O = Block("yellow", [[[1, 1],
                      [1, 1]]])

T = Block("magenta", [[[0, 0, 0],
                       [0, 1, 0],
                       [1, 1, 1]],

                      [[0, 1, 0],
                       [1, 1, 0],
                       [0, 1, 0]],

                      [[0, 0, 0],
                       [1, 1, 1],
                       [0, 1, 0]],

                      [[1, 0, 0],
                       [1, 1, 0],
                       [1, 0, 0]]])

tile_size = 25
map_rows = 20
map_cols = 10
map_x = -125
map_y = 250

map_turtle = turtle.Turtle()
map_turtle.hideturtle()
map_turtle.up()

game_map = [["" for _ in range(map_cols)] for _ in range(map_rows)]

active_block = None
active_block_row = 0
active_block_col = 0
active_block_index = 0

block_turtle = turtle.Turtle()
block_turtle.hideturtle()
block_turtle.up()

game_update_interval = 250

score = 0
score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.up()
score_turtle.goto(170, 210)
score_turtle.write("Score: " + str(score), font=("Calibri", 20, "bold"))

game_over_turtle = turtle.Turtle()
game_over_turtle.hideturtle()
game_over_turtle.color("red")


def draw_box(t, width, height, pencolor, fillcolor):
    t.color(pencolor, fillcolor)
    t.down()
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()
    t.up()


def draw_map():
    map_turtle.clear()
    for row in range(map_rows):
        for col in range(map_cols):
            map_turtle.goto(map_x + tile_size * col, map_y - tile_size * row)
            draw_box(map_turtle, tile_size, tile_size, "black",
                     game_map[row][col].color if game_map[row][col] else "mintcream")


def make_new_block():
    global active_block
    global active_block_row, active_block_col
    global active_block_index

    active_block = random.choice((I, J, L, S, Z, O, T))
    active_block_row = 0
    active_block_col = 4
    active_block_index = 0


def draw_block():
    block_turtle.clear()

    # Find the x and y position of the block
    x = map_x + active_block_col * tile_size
    y = map_y - active_block_row * tile_size

    block_tiles = active_block.tiles[active_block_index]
    block_color = active_block.color
    for row in range(len(block_tiles)):
        for col in range(len(block_tiles[row])):
            if block_tiles[row][col] == 1:
                block_turtle.goto(x + col * tile_size, y - row * tile_size)
                draw_box(block_turtle, tile_size, tile_size, "black", block_color)


def is_valid_block(block_type, block_row, block_col, block_index):
    block_tiles = block_type.tiles[block_index]
    for row in range(len(block_tiles)):
        for col in range(len(block_tiles[row])):
            if block_tiles[row][col] == 1:
                if block_row + row not in range(0, map_rows):
                    return False
                if block_col + col not in range(0, map_cols):
                    return False
                if game_map[block_row + row][block_col + col] != "":
                    return False

    return True


def set_block_on_map():
    block_tiles = active_block.tiles[active_block_index]
    for row in range(len(block_tiles)):
        for col in range(len(block_tiles[row])):
            if block_tiles[row][col] == 1:
                game_map[active_block_row + row][active_block_col + col] = active_block
    draw_map()


r = 0


def remove_completed_rows():
    global game_map
    global score
    global game_update_interval
    global r

    new_map = []
    for row in range(len(game_map)):
        game_row = game_map[row]
        if "" in game_row:
            new_map.append(game_row)
        else:
            score += 10
            score_turtle.clear()
            score_turtle.write("Score: " + str(score), font=("Calibri", 20, "bold"))
            r += 1
            if r == 5:
                game_update_interval = int(game_update_interval / 1.1)
                r = 0

    for row in range(0, map_rows - len(new_map)):
        game_row = ["" for _ in range(map_cols)]
        new_map.insert(0, game_row)

    game_map = new_map
    draw_map()

    # Task: increase the score and difficulty when a row is completed


pause = False


def game_loop():
    global active_block, active_block_row

    if active_block is None:
        make_new_block()
        if not is_valid_block(active_block, active_block_row, active_block_col, active_block_index):
            active_block = None
            game_over_turtle.write("Game over!", align="center", font=("Calibri", 60, "bold"))
            return
        draw_block()

    else:
        if is_valid_block(active_block, active_block_row + 1, active_block_col, active_block_index):
            if not pause:
                active_block_row += 1
                draw_block()
        else:
            set_block_on_map()
            active_block = None
            remove_completed_rows()

    turtle.update()

    # Set the next update

    turtle.ontimer(game_loop, game_update_interval)


# Set up the turtle window
turtle.setup(800, 600)
turtle.title("俄罗斯方块")
turtle.bgcolor("navajowhite")
turtle.up()
turtle.hideturtle()
turtle.tracer(False)

# Draw the background border around the map
turtle.goto(map_x - 10, map_y + 10)
draw_box(turtle, tile_size * map_cols + 20, tile_size * map_rows + 20, \
         "", "lightslategray")

# Draw the empty map in the window
draw_map()
turtle.update()

# Set up the game loop
turtle.ontimer(game_loop, game_update_interval)


def rotate():
    global active_block_index

    if active_block is None:
        return
    new_block_index = (active_block_index + 1) % len(active_block.tiles)
    if is_valid_block(active_block, active_block_row, active_block_col, new_block_index):
        active_block_index = new_block_index
        draw_block()


turtle.onkeypress(rotate, "Up")


def move_left():
    global active_block_col

    if active_block is None:
        return
    if is_valid_block(active_block, active_block_row, active_block_col - 1, active_block_index):
        active_block_col -= 1
        draw_block()


turtle.onkeypress(move_left, "Left")


def move_right():
    global active_block_col

    if active_block is None:
        return
    if is_valid_block(active_block, active_block_row, active_block_col + 1, active_block_index):
        active_block_col += 1
        draw_block()


turtle.onkeypress(move_right, "Right")


def drop():
    global active_block_row

    if active_block is None:
        return
    while is_valid_block(active_block, active_block_row + 1, active_block_col, active_block_index):
        active_block_row += 1
    draw_block()


turtle.onkeypress(drop, "Down")


def pause_game():
    global pause
    pause = not pause


turtle.onkeypress(pause_game, "space")


def change_block_type():
    global active_block
    global active_block_index

    new_block = random.choice((I, J, L, S, Z, O, T))
    new_block_index = 0
    if is_valid_block(new_block, active_block_row, active_block_col, new_block_index):
        active_block = new_block
        active_block_index = new_block_index
        draw_block()


turtle.onkeypress(change_block_type, "c")

turtle.listen()

turtle.done()
