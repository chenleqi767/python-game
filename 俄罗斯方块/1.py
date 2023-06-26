import os
import pygame
import sys
import random
import pygame.font
import time

pygame.init()

clos = 10  # 游戏网格列数，可以调整，>=8
rows = 20  # 游戏网格行数，可以调整
cell_size = 40  # 一个网格的大小
block_size = cell_size - 1  # 一个方块的大小,小于等于cell_size
block_edge = int(block_size / 2)  # 方块的立体感，数字>=1,数字越小立体感越强
fps = 40  # 每秒帧数，建议范围20-60，越大难度递进越越缓

win_width = clos * 2 * cell_size + 6 * cell_size
win_hight = (rows + 1) * cell_size
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 40)
screen = pygame.display.set_mode((win_width, win_hight))
pygame.display.set_caption("Crystal方块")

# 在4*4的小网格内，以左上角坐标为（0,0），7种方块及其各形态4个方块在小网格的相对坐标
# 移动时记录小网络（0,0）点在游戏网格的（x,y)，就知道4个方块在游戏网格中的位置
blocks = {
    1: [[(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)]],  # I型
    2: [[(1, 1), (2, 1), (1, 2), (2, 2)]],  # O型
    3: [[(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
        [(1, 1), (0, 2), (1, 2), (2, 2)],
        [(1, 0), (1, 1), (2, 1), (1, 2)]],  # T型
    4: [[(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(2, 1), (0, 2), (1, 2), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 2)]],  # L型
    5: [[(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
        [(0, 1), (0, 2), (1, 2), (2, 2)],
        [(1, 0), (2, 0), (1, 1), (1, 2)]],  # J型
    6: [[(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)]],  # s型
    7: [[(0, 1), (1, 1), (1, 2), (2, 2)],
        [(2, 0), (1, 1), (2, 1), (1, 2)]], }  # Z型

# 第1个为网格底色，后7个为对应方块的颜色，因为要加和原色相近的明暗边，自定义色RGB值最小得不低于50，最高不超过205，否则出错。
# 最后一个颜色（灰）用来画NEXT方块，也可以用NEXT方块的next_key值来指向本色
block_color = [(199, 238, 206), (200, 50, 50), (50, 200, 200), (50, 50, 200), (200, 200, 50), (200, 50, 200),
               (50, 200, 50), (125, 50, 125), (180, 180, 180)]


class Game_machine():
    def __init__(self, x0, y0):
        self.x0, self.y0 = x0, y0  # 记录player游戏区（0，0）点在屏幕的坐标
        self.rect = pygame.Rect(0, 0, block_size, block_size)  # 方块矩形大小
        self.display_array = [[0 for i in range(clos)] for j in range(rows)]  # 游戏区每格初始值设为0，为1时不能通过
        self.color_array = [[0 for i in range(clos)] for j in range(rows)]  # 游戏区每格的颜色block_color的索引值
        self.x, self.y = 0, 0  # 记录移动方块（0，0）点在游戏网格的（clo,row)位置
        self.key = 0  # 记录移动方块在blocks的键，是哪种方块
        self.index_ = 0  # 记录移动方块形态的索引
        self.next_key = self.rand_key()  # 记录NEXT方块在blocks的键
        self.speed = fps  # 速度，和帧率一致
        self.fall_buffer = self.speed  # 自动下落的缓冲时间，屏幕每刷一次自动减1
        self.fall_speed_up = False  # 是否加速下落
        self.score = 0
        self.lines = 0
        self.level = 0
        self.creat_new_block()

    def creat_new_block(self):
        # 产生新的移动方块和NEXT方块，以第一形态作为初始形态
        self.key = self.next_key
        self.next_key = self.rand_key()
        self.index = 0
        self.x = 4  # 初始列设在第4列
        self.y = -1  # 初始高度设为-1,保证方块在最顶部位置出现，研究每种方块第一形态坐标可以找到答案

    def rand_key(self):
        keys = [1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 7, 7]  # 决定每种方块出现概率
        return keys[random.randint(0, len(keys) - 1)]

    def move(self, dx, dy):
        # 方块左、右、下移动：左：dx=-1,dy=0  右:dx=1,dy=0  下：dx=0,dy=1
        if self.can_move(self.index, dx, dy):
            self.x += dx
            self.y += dy
        elif dy:
            # 不能下落：在顶部位置不能下落，游戏结束，以下位置则停止移动
            if self.y <= 0:
                self.game_over()
            else:
                self.stop_move()

    def rotate(self):
        # 方块旋转至下一形态，使用的顺时针旋转，被注释的是逆时针旋转
        next_index = (self.index + 1) % len(blocks[self.key])
        # next_index = (self.index - 1 + len(blocks[self.key])) % len(blocks[self.key])
        if self.can_move(next_index, 0, 0):
            self.index = next_index

    def can_move(self, index, dx, dy):
        # 方块能否移动:出界或碰到其他方块
        for (x, y) in blocks[self.key][index]:
            clo, row = self.x + x + dx, self.y + y + dy
            if clo >= clos or clo < 0 or row >= rows or row < 0:  # 出界
                return False
            if self.display_array[row][clo]:  # 值等于1时不能移动
                return False
        return True

    def stop_move(self):
        # 方块停止移动，停落区域赋值1和相应的颜色
        self.score += 4
        for (x, y) in blocks[self.key][self.index]:
            self.display_array[y + self.y][x + self.x] = 1
            self.color_array[y + self.y][x + self.x] = self.key
        self.del_full_row()
        self.creat_new_block()

    def del_full_row(self):
        # 删除填满的行，记录成绩
        lines = 0
        for row in range(rows):
            if sum(self.display_array[row]) == clos:  # 填满行判断
                lines += 1  # 记录一次连续删除的行数，实现多消多奖
                self.lines += 1
                if self.lines % 5 == 0:  # 每消5行等级升1，速度加快
                    self.level = self.lines / 5
                    self.speed = int(self.speed * 0.9)  # 越小越快
                self.score += (self.level + clos * lines) * 5

                del self.display_array[row]
                self.display_array.insert(0, [0 for i in range(clos)])

    def display(self):
        self.display_stop_blocks()
        self.display_next_blocks()
        self.display_move_blocks()
        self.display_score()

        # 每刷一次缓冲计数减1，缓冲计数=0，或按住了向下键则下落一格
        self.fall_buffer -= 1
        if self.fall_buffer == 0 or self.fall_speed_up:
            self.fall_buffer = self.speed
            self.move(0, 1)

    def display_stop_blocks(self):
        # 显示不移动的方块，值为1画彩色立体方块，值为0画底色块
        for y in range(rows):
            for x in range(clos):
                self.rect.topleft = x * cell_size, y * cell_size
                if self.display_array[y][x]:
                    self.draw_block(self.color_array[y][x], 1)
                else:
                    self.draw_block(0, 0)

    def display_next_blocks(self):
        # 显示下一个方块
        for (x, y) in blocks[self.next_key][0]:
            self.rect.topleft = x * cell_size, (y - 1) * cell_size
            self.draw_block(8, 1)

    def display_move_blocks(self):
        # 显示移动的方块
        for (x, y) in blocks[self.key][self.index]:
            self.rect.topleft = (self.x + x) * cell_size, (self.y + y) * cell_size
            self.draw_block(self.key, 1)

    def display_score(self):
        # 显示得分记录
        text = "得分：%d  行数：%d  等级：%d" % (self.score, self.lines, self.level)
        self.img = pygame.font.SysFont("kaiti", 25).render(text, True, (0, 0, 255))
        self.img_rect = self.img.get_rect()
        self.img_rect.topleft = (self.x0, rows * cell_size)
        screen.blit(self.img, self.img_rect)

    def game_over(self):
        # 只是简单的数据重新初始化后立即重新开始
        self.__init__(self.x0, self.y0)

    def draw_block(self, color_index, draw_edge):
        # 在指定位置画方块
        (r, g, b) = block_color[color_index]
        self.rect.centerx = self.rect.left + self.x0 + int(cell_size / 2)
        self.rect.centery = self.rect.top + self.y0 + int(cell_size / 2)
        if draw_edge:
            # 画方块明暗过度边，增加立体感，x0~x4是方块四角和中心的坐标。
            x0 = self.rect.center
            x1 = self.rect.topleft
            x2 = self.rect.topright
            x3 = self.rect.bottomright
            x4 = self.rect.bottomleft
            pygame.draw.polygon(screen, (r + 50, g + 50, b + 50), (x0, x1, x2), 0)
            pygame.draw.polygon(screen, (r + 20, g + 20, b + 20), (x0, x2, x3), 0)
            pygame.draw.polygon(screen, (r - 50, g - 50, b - 50), (x0, x3, x4), 0)
            pygame.draw.polygon(screen, (r - 20, g - 20, b - 20), (x0, x4, x1), 0)
            pygame.draw.rect(screen, (r, g, b), self.rect.inflate(-block_edge, -block_edge), 0)
        else:
            pygame.draw.rect(screen, (r, g, b), self.rect, 0)


time = pygame.time.Clock()
player1 = Game_machine(0, 0)
player2 = Game_machine((clos + 6) * cell_size, 0)

while True:
    time.tick(fps)
    screen.fill((166, 124, 64))
    player1.display()
    player2.display()
    pygame.display.update()

    # 移动旋转控制
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:  # player1 :g键右移动一格
                player1.move(1, 0)
            elif event.key == pygame.K_d:  # player1 :d键左移动一格
                player1.move(-1, 0)
            elif event.key == pygame.K_r:  # player1 :r键旋转一次
                player1.rotate()
            elif event.key == pygame.K_f:  # player1 :f键加速下移
                player1.fall_speed_up = True

            if event.key == pygame.K_RIGHT:  # player2 :→键右移动一格
                player2.move(1, 0)
            elif event.key == pygame.K_LEFT:  # player2 :←键左移动一格
                player2.move(-1, 0)
            elif event.key == pygame.K_UP:  # player2 :↑键旋转一次
                player2.rotate()
            elif event.key == pygame.K_DOWN:  # player2 :↓键加速下移
                player2.fall_speed_up = True

            elif event.key == pygame.K_q:
                sys.exit()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                player1.fall_speed_up = False
            if event.key == pygame.K_DOWN:
                player2.fall_speed_up = False
        elif event.type == pygame.QUIT:
            sys.exit()

