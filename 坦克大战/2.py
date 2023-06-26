# encoding : utf-8
# anthor : comi
from gameloop import *
from pygame import *
import pygame, sys, time

if __name__ == '__main__':
    player = game()  # 声明一个类对象
    player.game_start('KEEP-GOING')  # 调用开始函数
    while player.playing:  # 进入游戏运行
        player.new()  # 开始游戏
    player.screen.fill(black)
    player.game_start('GAME-OVER')  # 游戏结束
    time.sleep(1.5)  # 可以不要

# encoding : utf-8
# author : comi
from setting import *
from pygame import *
from Sprite import *
import pygame, sys

vec = pygame.math.Vector2


class game:  # 游戏类 包含循环等
    def __init__(self):  # 初始化
        pygame.init()  # pygame 初始化
        pygame.display.set_caption("Keep-Going")  # 游戏窗口 左上角名称
        self.screen = pygame.display.set_mode((width, height))  # 游戏窗口的大小
        self.FpsClock = pygame.time.Clock()  # 设置游戏的刷新率
        self.playing = True  # 进入游戏的状态
        self.running = True  # 游戏运行的状态
        self.Waiting = True  # 游戏等待的状态
        self.Pblood = 100  # 玩家血量
        self.Eblood = 100  # 敌人血量
        self.player = Player()  # 声明一个游戏玩家对象
        self.enemy = Enemy()  # 声明一个敌人对象
        self.all_groups = pygame.sprite.Group()  # 通过pygame自带的 group 来判断碰撞检测
        self.player_groups = pygame.sprite.Group()
        self.Map_groups = pygame.sprite.Group()
        self.Enemy_groups = pygame.sprite.Group()

    def new(self):  # 开始一个游戏
        self.player_groups.add(self.player)  # 将玩家添加到玩家组
        self.all_groups.add(self.player)  # 将玩家添加到 所有组

        self.Enemy_groups.add(self.enemy)
        self.all_groups.add(self.enemy)

        for platfroms in Map1:  # 地图
            p = Platform(*platfroms)  # 取出所有值
            self.Map_groups.add(p)
            self.all_groups.add(p)

        self.run()  # 调用函数运行游戏

    def game_start(self, text):  # 游戏的开始界面
        self.text_draw(width / 2, height / 4, 64, text)  # 文本
        self.text_draw(width / 2, height * 3 / 4, 25, 'Press any key to continue', )  # 文本
        pygame.display.update()  # 更行展示
        while self.Waiting:  # 实现 按键等待开始效果
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.Waiting = False

    def update(self):  # 画面更新
        self.Map_groups.update()
        self.player_groups.update()
        self.enemy.Bullet_groups.update(self.enemy.flag)  # 通过按键判断子弹方向
        self.player.Bullet_groups.update(self.player.flag)
        self.Enemy_groups.update()

        hit = pygame.sprite.groupcollide(self.player.Bullet_groups, self.Map_groups, True, False)  # 子弹碰墙消失
        hit = pygame.sprite.groupcollide(self.enemy.Bullet_groups, self.Map_groups, True, False)

        PMC = pygame.sprite.spritecollide(self.player, self.Map_groups, False, False)  # 撞墙
        if PMC:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_a]:
                self.player.pos.x = self.player.pos.x + gap
            if key_pressed[pygame.K_d]:
                self.player.pos.x = self.player.pos.x - gap
            if key_pressed[pygame.K_w]:
                self.player.pos.y = self.player.pos.y + gap
            if key_pressed[pygame.K_s]:
                self.player.pos.y = self.player.pos.y - gap

        EMC = pygame.sprite.spritecollide(self.enemy, self.Map_groups, False, False)  # 撞墙
        if EMC:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_LEFT]:
                self.enemy.pos.x = self.enemy.pos.x + gap
            if key_pressed[pygame.K_RIGHT]:
                self.enemy.pos.x = self.enemy.pos.x - gap
            if key_pressed[pygame.K_UP]:
                self.enemy.pos.y = self.enemy.pos.y + gap
            if key_pressed[pygame.K_DOWN]:
                self.enemy.pos.y = self.enemy.pos.y - gap

    def run(self):
        while self.running:
            self.FpsClock.tick(Fps)  # 设置帧率
            self.events()  # 获取事件
            self.draw_pic()  # 画出图片
            self.update()

            f
            self.Eblood <= 0:  # enemy
            self.screen.fill(black)
            self.game_start('P1 WIN!')
            time.sleep(1.5)
            self.running = False
            self.playing = False

        if self.Pblood <= 0:  # Player
            self.screen.fill(black)
            self.game_start('P2 WIN!')
            time.sleep(1.5)
            self.running = False
            self.playing = False


def text_draw(self, x, y, size, text):  # 文本展示函数
    self.font = pygame.font.Font('freesansbold.ttf', size)  # 字体，大小
    self.text_surf = self.font.render(text, True, red)  # 颜色
    self.text_rect = self.text_surf.get_rect()  # 矩形
    self.text_rect.center = (x, y)  # 位置
    self.screen.blit(self.text_surf, self.text_rect)  # 覆盖展示


def draw_pic(self):
    self.screen.fill(white)  # 背景
    self.text_draw(900, 50, 30, "KEEP")  # 文本
    self.text_draw(900, 100, 30, "GOING")

    self.text_draw(820, 150, 20, "P1:")
    self.text_draw(820, 200, 20, "P2:")

    self.text_draw(900, 250, 20, "Attention!")
    self.text_draw(900, 300, 20, "The Bullet Can")
    self.text_draw(900, 350, 20, "Be Control!")
    self.bar_draw(850, 145, self.Pblood)  # 血条
    hit = pygame.sprite.groupcollide(self.enemy.Bullet_groups, self.player_groups, True, False)  # 血条减少
    if hit:
        self.Pblood = self.Pblood - randint(10, 15)
        self.bar_draw(850, 145, self.Pblood)

    self.bar_draw(850, 195, self.Eblood)
    hit = pygame.sprite.groupcollide(self.player.Bullet_groups, self.Enemy_groups, True, False)
    if hit:
        self.Eblood = self.Eblood - randint(10, 15)
        self.bar_draw(850, 195, self.Eblood)

    self.Map_groups.draw(self.screen)  # 画出图片
    self.player_groups.draw(self.screen)
    self.Enemy_groups.draw(self.screen)
    self.player.Bullet_groups.draw(self.screen)
    self.enemy.Bullet_groups.draw(self.screen)

    pygame.display.update()


def bar_draw(self, x, y, pct):  # 血条函数
    # draw a bar
    if pct <= 0:
        pct = 0
    Bar_Lenth = 100
    Bar_Height = 10
    Fill_Lenth = (pct / 100) * Bar_Lenth
    Out_rect = pygame.Rect(x, y, Bar_Lenth, Bar_Height)
    Fill_rect = pygame.Rect(x, y, Fill_Lenth, Bar_Height)
    pygame.draw.rect(self.screen, green, Fill_rect)
    pygame.draw.rect(self.screen, red, Out_rect, 2)


def events(self):  # 事件
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            self.running = False
            self.playing = False


# encoding : utf-8
# antuor : comi
from setting import *
from pygame import *
import pygame, sys, time
from random import *
from math import *

vec = pygame.math.Vector2  # 运用向量


class Player(pygame.sprite.Sprite):  # 玩家类
    Bullet_groups = pygame.sprite.Group()
    flag = 1  # 判断方向的flag

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\down.png').convert()  # 图片的加载
        self.image.set_colorkey(white)  # 设置忽略白色
        self.rect = self.image.get_rect()
        self.rect.midbottom = (115, 130)

        self.pos = vec(115, 130)

        self.last_time = time.time()  # 记录上一次时间 用来设置子弹频率等

    def update(self):
        key_pressed = pygame.key.get_pressed()  # 按键获取
        if key_pressed[pygame.K_a]:
            self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\left.png').convert()
            self.image.set_colorkey(white)
            self.pos.x -= move_space  # 位置移动
            self.flag = 2
        if key_pressed[pygame.K_d]:
            self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\right.png').convert()
            self.image.set_colorkey(white)
            self.pos.x += move_space
            self.flag = 1
        if key_pressed[pygame.K_w]:
            self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\up.png').convert()
            self.image.set_colorkey(white)
            self.pos.y -= move_space
            self.flag = 3
        if key_pressed[pygame.K_s]:
            self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\down.png').convert()
            self.image.set_colorkey(white)
            self.pos.y += move_space
            self.flag = 4
        if key_pressed[pygame.K_SPACE]:
            self.shoot()
        self.rect.midbottom = self.pos

    def shoot(self):  # 开火
        self.now = time.time()  # 获取现在时间
        if self.now - self.last_time > 0.8:  # 子弹时间间隔
        # 这里显示错误了，应该在if 语句内 包含以下部分
        pygame.mixer.music.load(r'C:\Users\Administrator\Desktop\KeepGoing\sounds\expl.wav')
        pygame.mixer.music.play()  # 音乐加载
        bullet = Bullet(self.pos.x, self.pos.y)
        self.Bullet_groups.add(bullet)
        self.last_time = self.now


class Platform(pygame.sprite.Sprite):  # 地图创建
    def __init__(self, x, y, w, h):  # x，y，宽，高
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))  # 砖块大小
        self.image.fill(yellow)  # 砖颜色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):  # 与player 相同
    Bullet_groups = pygame.sprite.Group()
    flag = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\down.png').convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (315, 130)
        self.pos = vec(315, 130)
        self.bar = 100
        self.last_time = time.time()
        self.flag = 1

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\left.png').convert()
            self.image.set_colorkey(white)
            self.pos.x -= move_space
            self.flag = 2
        if key_pressed[pygame.K_RIGHT]:
            self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\right.png').convert()
            self.image.set_colorkey(white)
            self.pos.x += move_space
            self.flag = 1
        if key_pressed[pygame.K_UP]:
            self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\up.png').convert()
            self.image.set_colorkey(white)
            self.pos.y -= move_space
            self.flag = 3
        if key_pressed[pygame.K_DOWN]:
            self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\down.png').convert()
            self.image.set_colorkey(white)
            self.pos.y += move_space
            self.flag = 4
        if key_pressed[pygame.K_p]:
            self.shoot()

        self.rect.midbottom = self.pos

    def shoot(self):
        self.now = time.time()
        if self.now - self.last_time > 0.8:
            pygame.mixer.music.load(r'C:\Users\Administrator\Desktop\KeepGoing\sounds\expl.wav')
            pygame.mixer.music.play()
            bullet = Bullet(self.pos.x, self.pos.y)
            self.Bullet_groups.add(bullet)
            self.Bullet_groups.update(self.flag)
            self.last_time = self.now


class Bullet(pygame.sprite.Sprite):  # 炮弹组
    def __init__(self, x, y):  # 炮弹该有的位置 玩家周围
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\Administrator\Desktop\KeepGoing\img\dot.png ').convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 10  # 这里是准确的位置，未进行准确更改
        self.rect.bottom = y - 12
        self.speed = 5

    def update(self, flag):
        if flag == 1:  # right
            self.rect.x += self.speed
        if flag == 2:  # left
            self.rect.x -= self.speed
        if flag == 3:  # up
            self.rect.y -= self.speed
        if flag == 4:  # down
            self.rect.y += self.speed


# encoding : utf-8
# author ：comi
width = 1000
height = 600
Fps = 60
food = 20
gap = 3
move_space = 1.5
back_space = 5
Map1 = [(0, 0, width * 2, 10), (0, 10, 10, height * 2),
        (0, height - 10, width * 2, 10), (width - 210, 0, 10, height * 2),
        (50, 50, 100, 20), (250, 50, 100, 20), (150, 230, 100, 20), (100, 340, 200, 20),
        (50, 70, 20, 90), (130, 70, 20, 90), (250, 70, 20, 90), (330, 70, 20, 90),
        (130, 280, 20, 70), (250, 300, 20, 50),
        (80, 320, 20, 20), (300, 320, 20, 20), (185, 200, 30, 30), (185, 250, 30, 30),
        (60, 300, 20, 20), (320, 300, 20, 20),
        (40, 280, 20, 20), (340, 280, 20, 20),
        (490, 100, 160, 40), (650, 100, 40, 200), (425, 250, 150, 40), (425, 290, 40, 80),
        (510, 365, 160, 40), (695, 460, 95, 40), (595, 454, 40, 100), (190, 460, 30, 30),
        (300, 450, 200, 40), (100, 425, 30, 130), (200, 520, 230, 25), (725, 70, 30, 30),
        (725, 140, 30, 30), (725, 210, 30, 30), (725, 280, 30, 30), (725, 365, 30, 30)
        ]  # map
# color

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 200, 0)
purple = (128, 138, 135)

