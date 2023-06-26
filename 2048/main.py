# -*- coding: utf-8 -*-
# __/author__by:Kevin_F/__

import sys
import random
import pygame

matrix = []  # 二维数组，用于存放数字
list_zero = []  # 用一个集合去放矩阵中空的元素（即数字为0）的下标（x,y）
score = 0  # 得分
is_add = False  # 用于判断是否需要生成新的数字，默认不生成新数字
colors = {0: (205, 193, 180),  # 各种方块对应的颜色
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 98),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (225, 187, 0),
          4096: (225, 187, 0),
          8192: (225, 187, 0)
          }


#  初始化游戏界面
#  每个方块尺寸100*100，间隔15，整个矩阵上方留高150空间，用于显示得分和游戏结束的信息
def game_init():
    #  背景
    pygame.init()
    global screen
    screen = pygame.display.set_mode((475, 625))
    pygame.display.set_caption('Game-2048 by:Kevin_X    按ESC可重新开始游戏')
    screen.fill((255, 222, 173))
    #  得分区
    pygame.draw.rect(screen, (255, 239, 213), (0, 0, 475, 150), 0)
    font_defen = pygame.font.SysFont('SimHei', 50)
    text_defen = font_defen.render('得分', True, (205, 193, 180))
    screen.blit(text_defen, (40, 10))

    pygame.display.flip()


#  分数显示
def show_score(score):
    #   分数显示框
    pygame.draw.rect(screen, (255, 255, 255), (20, 70, 140, 70), 0)
    #   分数会不断累积变化
    font_score = pygame.font.SysFont('SimHei', 50)
    text_score = font_score.render(str(score), True, (255, 97, 0))
    tx2, ty2 = text_score.get_size()
    screen.blit(text_score, (90 - tx2 / 2, 105 - ty2 / 2))
    pygame.display.update()
    #    每次相加，分数都会发生变化，都需要重写  所以把分数显示单独开来，而不能跟游戏初始化放在一起
    #    分数显示框是一个矩形框，每次显示分数时，先重画矩形框，然后再写入分数值


#  初始化矩阵，用于存放数字
#  4*4的矩阵，共16个数字，0表示方块为空，不显示内容，其他数字正常显示数值
def _game_list():
    for i in range(4):  # 初始设置全为0
        lis = []
        for j in range(4):
            lis.append(0)
        matrix.append(lis)


#  显示游戏区域：游戏方块和数字
#  矩阵里每一个数字包含几个信息：数字内容，数字XY坐标，方块XY坐标，方块颜色，数字颜色，数字字体及大小
def show_game():
    for i in range(4):
        for j in range(4):
            """
            矩阵列表matrix[i][j]
            数字内容=matrix[i][j]           
            方块坐标block_x = 15+(15+100)*i =15+115*i
                   block_y=15+115*j
            数字坐标 根据方块坐标的起点和方块的大小算出方块中心点的坐标即数字中心点的坐标，然后再算出数字的起点坐标
            方块颜色根据数字内容取colors[matrix[i][j]]
            数字颜色 暂时固定为黑色，字体也固定大小50
            """

            block_color = colors[matrix[i][j]]
            #  方块的颜色，从字典colors里面，key即方块的数字，value即颜色
            block_pos = (15 + 115 * i, 15 + 115 * j)
            #  方块的位置
            pygame.draw.rect(screen, block_color, (15 + 115 * i, 165 + 115 * j, 100, 100), 0)
            pygame.display.update()
            #  绘制方块
            num_font = pygame.font.Font(None, 50)  # 数字字体
            num_color = (0, 0, 0)  # 数字颜色

            if matrix[i][j] != 0:  # 只有在方块里有数字时才会输出，方块是0时不显示
                num = num_font.render(str(matrix[i][j]), True, num_color)
                pos_num_x, pos_num_y = num.get_size()
                screen.blit(num, (65 + 115 * i - pos_num_x / 2, 215 + 115 * j - pos_num_y / 2))
                #  算出方块上显示的数字的原点坐标 （先求中心点的坐标，然后再减去长或者高的一半，得到起点坐标）
                #  x=15（方块到窗口边缘相距15）+50（方块长度的一半，方块中心点）-数字长度的一半
                #  y=150(得分区的高度)+间隔15+50（方块高度的一半）-数字高度的一半
                pygame.display.update()


#  空方格的x，y位置组成的列表的所有位置的列表
def empty():
    global list_zero
    list_zero = []
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:
                list_zero.append([i, j])


#  随机生成一个数字2或者4
def creatnum():
    global is_add
    empty()

    if list_zero and is_add:
        #  if list_zero 如果列表不为空的情况下才会生成数字
        #  如果列表为空，说明矩阵没有空元素，即矩阵每个方块都有数字，则没有位置生成新数字

        value = random.choice((2, 4))  # 这个是1:1的概率生成2和4
        # value=4 if random.randint(0,3)>2 else 2
        #  2和4生成的概率时3:1

        postion_zero = random.choice(list_zero)
        #  从list_zero这个列表里随机取一个元素，即从所有没有数字的方块中随机选一个
        #  list_zero里每一个元素都是一个列表，里面存放着[x,y]坐标
        matrix[postion_zero[0]][postion_zero[1]] = value
        #  将这个[x,y]坐标坐标给matrix[x][y]这样就能具体定位到矩阵的一个方块

        is_add = False
        #  每次生成一个新数字之后，把is_add属性改成False
        empty()
        #  因为随机生成了一个数（2或者4），list_zero的内容发生了变化，所以需要运行empty() 清空list_zero,然后重新生成0元素的list_zero
    else:
        pass


def Move_up():
    #  向上移动，可以看作每一列从上到下4个数字的移动，
    #  如果上面的数字是0即空格，则下面的非0数字上移填充空格位置
    #  如果上下两个非0元素相加，则上面元素翻倍，下面元素变成空格
    global score
    global is_add

    is_add = False
    #  先默认不生成新数字

    for x in range(4):
        #  向上移动，作用对象是每一列上下4个元素，所以最外面for循环是对x（横坐标），得到4列
        temp_list = [matrix[x][0], matrix[x][1], matrix[x][2], matrix[x][3]]
        #  或者用deepcopy，但不能用temp_list=matrix[x]，如果用等号赋值，相当于复制了内存地址，但内容没有复制，后面比较时永远是相等的
        #  创建一个临时列表，然后复制这一列的值
        #  有可能会出现按了向上移动的按键，但是没有任何一个方块发生移动，也没有任何数字相加（比如数字都集中在上面部分）
        #  即相当于按了向上键矩阵没有任何变化，此时应该不产生任何动作，而不能生成新数字
        #  这个时候就需要比较按键之后和按键之前，matrix矩阵有没有发生变化
        while 0 in matrix[x]:
            matrix[x].remove(0)
            #  先将每一列中的0元素删除，即空格删除，得到数字
        if len(matrix[x]) >= 2:
            #  如果只剩下一行，那就没办法比较，会报错下标越界
            #  只有在有至少两行的情况下，才能比较本行与下一行的数字是否相等
            for i in range(0, len(matrix[x]) - 1):
                if matrix[x][i] == matrix[x][i + 1]:
                    #  如果本数字与下面数字相等，则会发生相加动作
                    #  因为是向上移动，发生相加时，靠上的数字翻倍，靠下的数字变成空格
                    matrix[x][i] *= 2
                    matrix[x][i + 1] = 0
                    is_add = False
                    #  如果发生相加，则不生成新数字，所以要改属性为False
                    score += matrix[x][i]
                    #  得分累加

            #  这个for循环结束后，会把相同的非0元素相加，相加即靠上的元素*2，靠下的元素变成0，因此会产生元素0
            #  再用一次while循环 去0
            while 0 in matrix[x]:
                matrix[x].remove(0)

        while len(matrix[x]) < 4:
            matrix[x].append(0)
        if temp_list != matrix[x]:
            is_add = True
            #  判断  只要for循环中有任意一列与之前不同，说明发生了移动，则需要生成新数字
            #  相反，如果所有列在移动前后都一样，则说明没有移动，即按键没反应，不需要生成新数字
    creatnum()
    #  执行生成新数字（关键看is_add属性）
    show_game()
    #  重新生成矩阵方块和数字
    show_score(score)
    #  刷新得分


def Move_down():
    global score
    global is_add

    is_add = False
    for x in range(4):
        temp_list = [matrix[x][0], matrix[x][1], matrix[x][2], matrix[x][3]]
        while 0 in matrix[x]:
            matrix[x].remove(0)
        if len(matrix[x]) >= 2:  # 如果只剩下一行，那就没办法比较，会报错下标越界
            for i in range(0, len(matrix[x]) - 1):
                if matrix[x][i] == matrix[x][i + 1]:
                    matrix[x][i + 1] *= 2
                    matrix[x][i] = 0
                    is_add = False
                    score += matrix[x][i + 1]
                    #  如果发生相加，则不生成新数字

            #  这个for循环结束后，会把相同的非0元素相加，相加即靠下的元素*2，靠上的元素变成0，因此会产生元素0
            #  再用一次while循环 去0
            while 0 in matrix[x]:
                matrix[x].remove(0)

        while len(matrix[x]) < 4:
            matrix[x].insert(0, 0)
            #  向下移动时，需要在上面补0，所以用insert在列表0即开头的位置插入数字0，补全列表4个数
        if temp_list != matrix[x]:
            is_add = True
            #  判断  只要for循环中有任意一列与之前不同，说明发生了移动，则需要生成新数字
            #  如果所有列在移动前后都一样，则说明没有移动，即按键没反应，不需要生成新数字
    creatnum()
    show_game()
    show_score(score)


def Move_left():
    global score
    global is_add

    is_add = False
    for y in range(4):
        row_list = [matrix[0][y], matrix[1][y], matrix[2][y], matrix[3][y]]
        temp_list = [matrix[0][y], matrix[1][y], matrix[2][y], matrix[3][y]]
        #  横向一行提取元素出来，重新组成一个数组row_list
        #  同时，复制一个一样的temp_list，为了对比按下向下的按键之后是否有元素发生移动
        while 0 in row_list:
            row_list.remove(0)
            #  列表去0
        if len(row_list) >= 2:  # 如果只剩下一行，那就没办法比较，会报错下标越界
            for i in range(0, len(row_list) - 1):
                if row_list[i] == row_list[i + 1]:
                    #  向左移，如果相邻的两个元素相等  那么前一个元素*2，后一个元素变成0
                    #  不能直接删除元素，如果用del删除元素，则row_list这个列表就变短了，下标也对应会-1，再for循环时有可能越界
                    row_list[i] *= 2
                    row_list[i + 1] = 0
                    is_add = False
                    #  如果发生相加，则不会生成新数字，改is_add的值
                    score += row_list[i]
                    #  积分累加

            #  再用一次while循环 去0
            while 0 in row_list:
                row_list.remove(0)

        while len(row_list) < 4:
            row_list.append(0)
            #  因为是向左移，所以在后面补0直到补全4个数字

        #  把row_list这一行的4个数字重新写入矩阵列表matrix
        for i in range(4):
            matrix[i][y] = row_list[i]

        if temp_list != row_list:
            is_add = True
            #  判断  只要for循环中有任意一行与之前不同，说明发生了移动，则需要生成新数字
            #  如果所有行在移动前后都一样，则说明没有移动，即按键没反应，不需要生成新数字

    creatnum()
    show_game()
    show_score(score)


def Move_right():
    global score
    global is_add

    is_add = False
    for y in range(4):
        row_list = [matrix[0][y], matrix[1][y], matrix[2][y], matrix[3][y]]
        temp_list = [matrix[0][y], matrix[1][y], matrix[2][y], matrix[3][y]]
        #  横向一行提取元素出来，重新组成一个数组row_list
        #  同时，复制一个一样的temp_list，为了对比按下向下的按键之后是否有元素发生移动
        while 0 in row_list:
            row_list.remove(0)
            #  列表去0
        if len(row_list) >= 2:  # 如果只剩下一行，那就没办法比较，会报错下标越界
            for i in range(0, len(row_list) - 1):
                if row_list[i] == row_list[i + 1]:
                    #  向右移，如果相邻的两个元素相等  那么前一个元素=0，后一个元素*2
                    #  不能直接删除元素，如果用del删除元素，则row_list这个列表就变短了，下标也对应会-1，再for循环时有可能越界
                    row_list[i + 1] *= 2
                    row_list[i] = 0
                    is_add = False
                    #  如果发生相加，则不会生成新数字，改is_add的值
                    score += row_list[i + 1]
                    #  积分累加

            #  再用一次while循环 去0
            while 0 in row_list:
                row_list.remove(0)

        while len(row_list) < 4:
            row_list.insert(0, 0)
            #  因为是向右移，所以在最前面补0直到补全4个数字

        #  把row_list这一行的4个数字重新写入矩阵列表matrix
        for i in range(4):
            matrix[i][y] = row_list[i]

        if temp_list != row_list:
            is_add = True
            #  判断  只要for循环中有任意一行与之前不同，说明发生了移动，则需要生成新数字
            #  如果所有行在移动前后都一样，则说明没有移动，即按键没反应，不需要生成新数字

    creatnum()
    show_game()
    show_score(score)


#  判断游戏是否结束
def is_gameover():
    #  本游戏没有赢的时候，只有最高分（16格最终会被填满）
    #  只要有格子没有数字，即数字为0 ，则游戏一定没有结束
    #  当横向、竖向相邻两两比较，只要出现任一相等，游戏没有结束
    if list_zero:
        #  list_zero里面装的是数字0，只要list_zero非空，则说明肯定有空格，直接判断游戏没有结束
        return False
    else:
        #  竖向每一列检查
        for i in range(4):
            for j in range(3):
                if matrix[i][j] == matrix[i][j + 1]:
                    return False
        #  横向每一行检查
        for j in range(4):
            for i in range(3):
                if matrix[i][j] == matrix[i + 1][j]:
                    return False
        return True
        #  如果两次for循环都执行结束，则说明横竖相邻两两都不一样，游戏结束


# 定义主函数
def main():
    global is_add, matrix, list_zero, score
    matrix = []
    list_zero = []
    score = 0
    is_add = False
    #  初始化
    game_init()
    _game_list()
    show_game()

    is_add = True
    creatnum()
    #  随机生成一个数
    is_add = True
    creatnum()
    #  再随机生成一个数
    #  棋盘上有两个数，游戏才开始玩

    show_game()
    show_score(score)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not is_gameover():  # 如果游戏没有结束
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return main()
                        #  按ESC重新开始游戏

                    elif event.key == pygame.K_LEFT:
                        Move_left()

                    elif event.key == pygame.K_RIGHT:
                        Move_right()

                    elif event.key == pygame.K_UP:
                        Move_up()

                    elif event.key == pygame.K_DOWN:
                        Move_down()

                    else:
                        pass
            else:  # 如果游戏结束
                font_gameover = pygame.font.SysFont('SimHei', 60)
                text_gameover = font_gameover.render("游戏结束", True, (255, 0, 0))
                screen.blit(text_gameover, (220, 45))
                pygame.display.update()


if __name__ == '__main__':
    main()


