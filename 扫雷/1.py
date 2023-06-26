from os import abort
import pygame, random as r, time, sys, easygui as e

coveredImg = pygame.image.load('images/covered.png')
flagedImg = pygame.image.load('images/flaged.png')
uncoverImg = {}
for i in range(9):
    uncoverImg[i] = pygame.image.load('images/uncover_' + str(i) + '.png')

# 基础搭建
x, y, boomnum = e.multenterbox(msg='建议参数：10，10，10', title='自定义参数', \
                               fields=['长', '宽', '雷'], values=['10', '10', '10'])
x, y, boomnum = int(x), int(y), int(boomnum)
pygame.init()
canvas = pygame.display.set_mode((x * 32, y * 32))
pygame.display.set_caption('扫雷')

event = []


def handleEvent():
    global events, mousePos, cells
    mousePos = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                cells[int(mousePos[0] / 32)][int(mousePos[1] / 32)].discover()
            elif e.button == 3:
                cells[int(mousePos[0] / 32)][int(mousePos[1] / 32)].fmC()


class Cell():
    def __init__(self, x, y, coverMode, boomMode, flagMode):
        self.x = x
        self.y = y
        self.cm = coverMode
        self.bm = boomMode
        self.fm = flagMode

    def discover(self):
        if self.bm == True:  # 是雷关闭窗口
            pygame.quit()
            sys.exit()
        ab = self.checkAround()
        self.cm = ab
        if ab == 0:
            for x in range(self.x - 1, self.x + 2):
                for y in range(self.y - 1, self.y + 2):  # 遍历一圈
                    try:
                        cell = cells[x][y]
                        if cell.cm == 'True':
                            cells[x][y].discover()
                    except:
                        pass

    def checkAround(self):
        aroundBooms = 0
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):  # 遍历一圈
                try:  # 在角落时会有-1等值出现，唯一的报错源
                    if x == self.x and y == self.y:  # 是自身
                        pass
                    else:
                        if cells[x][y].bm:  # 如果是雷
                            aroundBooms += 1
                except:
                    pass
        return aroundBooms

    def fmC(self):
        self.fm = not self.fm


def create_map():
    global cells
    cells = {}
    for xi in range(x):
        cells[xi] = {}
        for yi in range(y):
            cells[xi][yi] = Cell(xi, yi, 'True', False, False)

    boomL = [0] * x * y
    for i in range(boomnum):
        boomL[i] = 1
    r.shuffle(boomL)

    for xi in range(x):
        for yi in range(y):
            if boomL[x * yi + xi] == 1:
                cells[xi][yi].bm = True


def display():
    for temp in cells.values():
        for cell in temp.values():
            displayImg = coveredImg
            if cell.fm == True:
                displayImg = flagedImg
            if cell.cm != 'True':
                displayImg = uncoverImg[cell.cm]
            canvas.blit(displayImg, (cell.x * 32, cell.y * 32))


def checkWin():
    tempV = True
    for temp in cells.values():
        for cell in temp.values():
            if cell.bm != True and cell.cm == 'True':
                tempV = False
    return tempV


create_map()
beginTime = time.time()
while True:
    print(int((time.time() - beginTime) * 100) / 100)
    display()
    handleEvent()
    pygame.display.update()
    if checkWin():
        break
finalTime = int((time.time() - beginTime) * 100) / 100
while True:
    print('你赢了，用时', finalTime, '秒！')
