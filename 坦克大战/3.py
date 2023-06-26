from pygame import *
import pygame,time,random
SCREEN_WIDTH = 900
SCRREN_HEIGHT = 600
COLOR_BLACK = pygame.Color(0,0,0)
VERSION = 'v2.5'
class MainGame():
    #游戏窗口
    window = None
    P1 = None
    #敌方坦克列表
    enemyTankList = []
    #我方子弹列表
    myBulletList = []
    #存储敌方子弹
    enemyBulletList = []
    #存储爆炸效果的列表
    bombList = []
    #存储墙壁的列表
    wallList = []
    def __init__(self):
        self.version = VERSION
    def startGame(self):
        print('游戏开始')
        #初始化展示模块
        pygame.display.init()
        #调用自定义的创建窗口的方法
        self.creatWindow()
        #设置游戏标题
        pygame.display.set_caption('坦克大战'+self.version)
        #调用创建墙壁的方法
        self.creatWalls()
        #调用创建坦克方法
        self.creatMyTank()
        #调用创建敌方坦克
        self.creatEnemyTank()
        while True:
            #设置游戏背景的填充色
            MainGame.window.fill(COLOR_BLACK)
            #调用展示墙壁的方法
            self.showAllWalls()
            # 调用展示我方坦克的方法
            self.showMyTank()
            #调用展示我方子弹的方法
            self.showAllMyBullet()
            #调用展示所有爆炸效果的方法
            self.showAllBombs()
            #调用展示敌方坦克的方法
            self.showEnemyTank()
            #调用展示敌方子弹的方法
            self.showAllEnemyBullet()
            #调用获取事件，处理事件的方法
            self.getAllEvents()
            #窗口持续刷新以即时显示
            pygame.display.update()
            time.sleep(0.02)
    def creatWindow(self):
        MainGame.window = pygame.display.set_mode((SCREEN_WIDTH,SCRREN_HEIGHT))
    def getAllEvents(self):
        #获取所有的事件
        event_list = pygame.event.get()
        for e in event_list:
            if e.type == pygame.QUIT:
                #关闭窗口，结束游戏，调用gameOver方法
                self.gameOver()
            elif e.type == pygame.KEYDOWN:
                print('点击键盘按键')
                if e.key == pygame.K_SPACE:
                    bullet = MainGame.P1.shot()
                    #控制子弹发射的数量
                    if len(MainGame.myBulletList) < 4:
                        print('发射子弹')
                        MainGame.myBulletList.append(bullet)
                        print('当前我方子弹数量为:',len(MainGame.myBulletList))
                        #创建音效对象，播放音效文件
                        audio = Audio('tank-images/boom.wav')
                        audio.play()
    #创建墙壁的方法
    def creatWalls(self):
        for i in range(1,8):
            wall = Wall(i*120,380,'tank-images/steels.gif')
            MainGame.wallList.append(wall)
    #展示墙壁的方法
    def showAllWalls(self):
        for w in MainGame.wallList:
            w.displayWall()

    def creatMyTank(self):
        MainGame.P1 = MyTank(SCREEN_WIDTH/2,SCRREN_HEIGHT/4*3)
    def showMyTank(self):
        MainGame.P1.displayTank()
        MainGame.P1.move()
        MainGame.P1.hitWalls()
    #展示我方子弹
    def showAllMyBullet(self):
        for b in MainGame.myBulletList:
            if b.live:
                b.displayBullet()
                #调用子弹的移动方法
                b.move()
                #调用是否打中敌方坦克的方法
                b.hitEnemyTank()
                #调用是否打中墙壁的方法
                b.hitWalls()
            else:
                MainGame.myBulletList.remove(b)
    #展示敌方子弹
    def showAllEnemyBullet(self):
        for b in MainGame.enemyBulletList:
            if b.live:
                b.displayBullet()
                b.move()
                #调用是否打中墙壁的方法
                b.hitWalls()
            else:
                MainGame.enemyBulletList.remove(b)
    def creatEnemyTank(self):
        for i in range(5):
            etank = EnemyTank(random.randint(1,8)*100,150)
            MainGame.enemyTankList.append(etank)
    def showEnemyTank(self):
        for etank in MainGame.enemyTankList:
            etank.displayTank()
            etank.move()
            etank.hitWalls()
            #调用射击方法
            etank.shot()
    #展示所有爆炸效果
    def showAllBombs(self):
        for bomb in MainGame.bombList:
            if bomb.live:
                bomb.displayBomb()
            else:
                MainGame.bombList.remove(bomb)
    def gameOver(self):
        print('游戏结束')
        exit()
class Tank():
    def __init__(self,x,y):
        #图片集(存储4个方向的所有图片)
        self.images = {
            'U':pygame.image.load('tank-images/tankU.gif'),
            'D':pygame.image.load('tank-images/tankD.gif'),
            'L':pygame.image.load('tank-images/tankL.gif'),
            'R':pygame.image.load('tank-images/tankR.gif'),
        }
        self.direction = 'U'
        #从图片集中根据方向获取图片
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 3
        self.isDead = False
        #新增属性用来记录上一步的坐标
        self.oldx = self.rect.centerx
        self.oldy = self.rect.centery
    def stay(self):
        self.rect.centerx = self.oldx
        self.rect.centery = self.oldy
    def hitWalls(self):
        index = self.rect.collidelist(MainGame.wallList)
        if index != -1:
            self.stay()
    def move(self):
        #记录移动之前的坐标
        self.oldx = self.rect.centerx
        self.oldy = self.rect.centery
        if self.direction == 'U':
            if self.rect.centery > self.rect.height/2:
                self.rect.centery -= self.speed
        elif self.direction == 'D':
            if self.rect.centery < SCRREN_HEIGHT - self.rect.height/2:
                self.rect.centery += self.speed
        elif self.direction == 'L':
            if self.rect.centerx > self.rect.height/2:
                self.rect.centerx -= self.speed
        elif self.direction == 'R':
            if self.rect.centerx < SCREEN_WIDTH - self.rect.height/2:
                self.rect.centerx += self.speed
    def shot(self):
        return Bullet(self)
    def displayTank(self):
        # 重新设置坦克图片
        self.image = self.images[self.direction]
        # 将坦克加载的到窗口
        MainGame.window.blit(self.image, self.rect)
class MyTank(Tank):
    def __init__(self,x,y):
        super(MyTank, self).__init__(x,y)
    def move(self):
        #pygame.key
        pressed_list = pygame.key.get_pressed()
        #分别判断上下左右四个方向的按键，按下的状态
        if pressed_list[pygame.K_LEFT]:
            #修改坦克的方向
            self.direction = 'L'
            super(MyTank, self).move()
        elif pressed_list[pygame.K_RIGHT]:
            self.direction = 'R'
            super(MyTank, self).move()
        elif pressed_list[pygame.K_UP]:
            self.direction = 'U'
            super(MyTank, self).move()
        elif pressed_list[pygame.K_DOWN]:
            self.direction = 'D'
            super(MyTank, self).move()
class EnemyTank(Tank):
    def __init__(self,x,y):
        super(EnemyTank, self).__init__(x,y)
        #随机速度
        self.speed = self.randSpeed(2,5)
        #随机方向
        self.direction = self.randDirection()
        #图片
        # self.image = self.images[self.direction]
        #坐标位置
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        #记录坦克移动步数的变量
        self.step = random.randint(25,50)
    #生成随机速度值
    def randSpeed(self,from_,to_):
        return random.randint(from_,to_)
    def randDirection(self):
        list1 = ['U','D','L','R']
        return list1[random.randint(0,3)]
    def move(self):
        if self.step > 0:
            super(EnemyTank, self).move()
            self.step -= 1
        else:
            #1.生成新的方向
            self.direction = self.randDirection()
            #2.步数还原
            self.step = random.randint(25,50)
    def shot(self):
        num = random.randint(1,40)
        if num == 1:
            b = Bullet(self)
            MainGame.enemyBulletList.append(b)
class Bullet():
    def __init__(self,tank):
        #图片
        if isinstance(tank,MyTank):
            self.image = pygame.image.load('tank-images/tankmissile.gif')
        else:
            self.image = pygame.image.load('tank-images/enemymissile.gif')
        #方向
        self.direction = tank.direction
        #坐标位置
        self.rect = self.image.get_rect()
        #子弹的具体位置
        if self.direction == 'U':
            self.rect.centerx = tank.rect.centerx
            self.rect.centery = tank.rect.centery - tank.rect.height/2 - self.rect.height/2
        elif self.direction == 'D':
            self.rect.centerx = tank.rect.centerx
            self.rect.centery = tank.rect.centery + tank.rect.height / 2 + self.rect.height / 2
        elif self.direction == 'L':
            self.rect.centery = tank.rect.centery
            self.rect.centerx = tank.rect.centerx - tank.rect.height/2 - self.rect.height/2
        elif self.direction == 'R':
            self.rect.centery = tank.rect.centery
            self.rect.centerx = tank.rect.centerx + tank.rect.height / 2 + self.rect.height / 2
        #移动速度
        self.speed = 8
        #子弹的状态（live）
        self.live = True
    def move(self):
        if self.direction == 'U':
            #边界控制
            if self.rect.centery > 0:
                self.rect.centery -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.centery < SCRREN_HEIGHT:
                self.rect.centery += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.centerx > 0:
                self.rect.centerx -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.centerx < SCREEN_WIDTH:
                self.rect.centerx += self.speed
            else:
                self.live = False
    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)
    #子弹与墙壁的碰撞
    def hitWalls(self):
        index = self.rect.collidelist(MainGame.wallList)
        if index != -1:
            self.live = False
    # 我方子弹是否碰撞到敌方坦克
    def hitEnemyTank(self):
        index = self.rect.collidelist(MainGame.enemyTankList)
        if index != -1:
            # 打中敌方坦克后的业务逻辑
            # 修改子弹的live属性
            self.live = False
            tank = MainGame.enemyTankList.pop(index)
            # 打中敌方坦克之后产生一个爆炸效果，装进爆炸效果列表中
            bomb = Bomb(tank)
            MainGame.bombList.append(bomb)
class Bomb():
    def __init__(self,tank):
        #存储多张爆炸效果的图片
        self.images = [
            pygame.image.load('tank-images/0.gif'),
            pygame.image.load('tank-images/1.gif'),
            pygame.image.load('tank-images/2.gif'),
            pygame.image.load('tank-images/3.gif'),
            pygame.image.load('tank-images/4.gif'),
            pygame.image.load('tank-images/5.gif'),
            pygame.image.load('tank-images/6.gif')
        ]
        #用来记录图片为图片集中的第几张
        self.index = 0
        self.image = self.images[self.index]
        self.live = True
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.rect.centerx
        self.rect.centery = tank.rect.centery
    def displayBomb(self):
        if self.index < len(self.images):
            self.image = self.images[self.index]
            self.index += 1
            MainGame.window.blit(self.image, self.rect)
        else:
            self.index = 0
            self.live = False
class Audio():
    def __init__(self,musicpath):
        pygame.mixer.init()
        pygame.mixer.music.load(musicpath)
    def play(self):
        pygame.mixer.music.play()
class Wall():
    def __init__(self,x,y,imagepath):
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)
game = MainGame()
game.startGame()