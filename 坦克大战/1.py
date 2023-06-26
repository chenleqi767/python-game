import pygame, time, random
from pygame.sprite import Sprite

# 定义常量
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)


# 创建精灵类
class BaseItem(Sprite):
    pass


# 主类
class Maingame():
    window = None
    mytanke = None
    enemyCount = 5
    enemyList = []
    myBulletlist = []
    enemybulletlist = []
    expllist = []
    wallslist = []

    # 初始化
    def __init__(self) -> None:
        pass

    # 创建敌方坦克
    def createEnemytanke(self):
        top = 100
        for i in range(Maingame.enemyCount):
            left = random.randint(0, 1200)
            speed = random.randint(1, 4)
            enemyTanke = enemytanke(left, top, speed)
            # 添加列表
            Maingame.enemyList.append(enemyTanke)

    # 加载敌方他坦克
    def displayenemytanke(self):
        for enemyTanke in Maingame.enemyList:
            if enemyTanke.live:
                enemyTanke.displayTanke()
                enemyTanke.randMove()
                # 初始化敌方子弹
                enemybullet = enemyTanke.shot()
                enemyTanke.tankehitwalls()
                if Maingame.mytanke and Maingame.mytanke.live:
                    enemyTanke.enemytkhitmytabke()
                if enemybullet:
                    Maingame.enemybulletlist.append(enemybullet)
            else:
                Maingame.enemyList.remove(enemyTanke)

    # 显示我方坦克子弹
    def displaymybullet(self):
        for myBullet in Maingame.myBulletlist:
            # 判断子弹是否存活
            if myBullet.live:
                myBullet.displaybullet()
                myBullet.bulletmove()
                myBullet.hitenemytanke()
                myBullet.hitwalls()
            else:
                Maingame.myBulletlist.remove(myBullet)

    # 显示敌方坦克子弹
    def displayenemybullet(self):
        for enemybullet in Maingame.enemybulletlist:
            if enemybullet.live:
                enemybullet.displaybullet()
                enemybullet.bulletmove()
                # 调用敌方子弹与我方坦克碰撞方法
                enemybullet.hitmytanke()
                enemybullet.hitwalls()
            else:
                Maingame.enemybulletlist.remove(enemybullet)

    # 展示爆炸效果
    def displayexpl(self):
        for expl in Maingame.expllist:
            if expl.live:
                expl.displayexplode()
            else:
                Maingame.expllist.remove(expl)

    # 创建我方坦克
    def createmytanke(self):
        Maingame.mytanke = mytanke(450, 600)

    # 创建墙壁方法
    def createwall(self):
        top = SCREEN_HEIGHT / 2
        for i in range(6):
            wall = Walls(i * 230, top)
            Maingame.wallslist.append(wall)

    # 展示墙壁的方法
    def displaywallslist(self):
        for wall in Maingame.wallslist:
            if wall.live:
                wall.displaywalls()
            else:
                Maingame.wallslist.remove(wall)

    # 开始游戏
    def sartgame(self):
        # 初始化窗口
        pygame.display.init()
        # 设置窗口大小
        Maingame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置窗口标题
        pygame.display.set_caption('坦克大战01')
        # 初始化我方坦克
        self.createmytanke()
        # 调用创建敌方坦克
        self.createEnemytanke()
        # 调用创建 墙壁方法
        self.createwall()
        while True:
            time.sleep(0.02)
            # 设置窗口填充色
            Maingame.window.fill(BG_COLOR)
            # 添加文字信息
            textSurface = self.getTextSurface('敌方坦克剩余数量%d' % len(Maingame.enemyList))
            # 添加主窗口显示文字信息
            Maingame.window.blit(textSurface, (10, 5))
            # 添加事件监听
            self.getEvent()
            # 调用坦克的显示方法
            if Maingame.mytanke and Maingame.mytanke.live:
                Maingame.mytanke.displayTanke()
            else:
                del Maingame.mytanke
                Maingame.mytanke = None
            # 调用坦克移动的方法
            if Maingame.mytanke and Maingame.mytanke.live:
                if not Maingame.mytanke.stop:
                    Maingame.mytanke.move()
                    Maingame.mytanke.tankehitwalls()
                    Maingame.mytanke.mytankehitenemytanke()
            # 加载敌方坦克
            self.displayenemytanke()
            # 加载我方子弹
            self.displaymybullet()
            # 加载敌方子弹
            self.displayenemybullet()
            # 加载爆炸效果
            self.displayexpl()
            # 加载墙壁
            self.displaywallslist()

            pygame.display.update()

    # 结束游戏
    def endgame(self):
        exit()

    # 添加文件信息提示
    def getTextSurface(self, text):
        # 初始化字体模块
        pygame.font.init()
        # 获取字体对象
        font = pygame.font.SysFont('kaiti', 18)
        # 绘制文字信息
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface

    # 添加事件监听
    def getEvent(self):
        # 获取事件
        eventlist = pygame.event.get()
        # 遍历事件
        for event in eventlist:
            # 判断按下的键是关闭还是键盘按下
            # 如果按下的是退出，关闭窗口
            if event.type == pygame.QUIT:
                self.endgame()
            if event.type == pygame.KEYDOWN:
                if not Maingame.mytanke:
                    if event.key == pygame.K_ESCAPE:
                        self.createmytanke()
                if Maingame.mytanke and Maingame.mytanke.live:
                    if event.key == pygame.K_LEFT:
                        Maingame.mytanke.direction = 'L'
                        # 修改坦克的移动开关
                        Maingame.mytanke.stop = False
                    elif event.key == pygame.K_RIGHT:
                        Maingame.mytanke.direction = 'R'
                        # 修改坦克的移动开关
                        Maingame.mytanke.stop = False
                    elif event.key == pygame.K_UP:
                        Maingame.mytanke.direction = 'U'
                        # 修改坦克的移动开关
                        Maingame.mytanke.stop = False
                    elif event.key == pygame.K_DOWN:
                        Maingame.mytanke.direction = 'D'
                        # 修改坦克的移动开关
                        Maingame.mytanke.stop = False
                    elif event.key == pygame.K_SPACE:
                        if len(Maingame.myBulletlist) < 5:
                            myBullet = bullet(Maingame.mytanke)
                            Maingame.myBulletlist.append(myBullet)

            # 判断键盘是否松开
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if Maingame.mytanke and Maingame.mytanke.live:
                        Maingame.mytanke.stop = True


# 坦克类
class Tanke(BaseItem):
    # 初始化
    def __init__(self, left, top) -> None:
        # 保存加载的图片
        self.images = {'U': pygame.image.load('img/U.png'),
                       'L': pygame.image.load('img/L.png'),
                       'R': pygame.image.load('img/R.png'),
                       'D': pygame.image.load('img/D.png')}
        # 设置坦克方向
        self.direction = 'L'
        # 根据坦克方向，获取加载的图片
        self.image = self.images.get(self.direction)
        # 根据图片获取图片的矩形区域
        self.rect = self.image.get_rect()
        # 设置区域的left和 top
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = 5
        # 坦克移动开关
        self.stop = True
        # 生存状态
        self.live = True
        # 移动之前的位置
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top

    # 展示坦克
    def displayTanke(self):
        self.image = self.images.get(self.direction)
        # 调用blit方法展示
        Maingame.window.blit(self.image, self.rect)

    # 移动
    def move(self):
        # 移动之前的位置
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        # 判断坦克的方向
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed

    # 射击
    def shot(self):
        pass

    # 设置坦克位置为移动之前的位置
    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop

    # 碰撞墙壁
    def tankehitwalls(self):
        for walls in Maingame.wallslist:
            if pygame.sprite.collide_rect(self, walls):
                self.stay()


# 我方坦克
class mytanke(Tanke):
    # 初始化
    def __init__(self, left, top) -> None:
        super(mytanke, self).__init__(left, top)

    # 碰撞敌方坦克
    def mytankehitenemytanke(self):
        for enemytanke in Maingame.enemyList:
            if pygame.sprite.collide_rect(self, enemytanke):
                self.stay()


# 敌方坦克
class enemytanke(Tanke):
    # 初始化
    def __init__(self, left, top, speed) -> None:
        # 调用父类初始化方法
        super(enemytanke, self).__init__(left, top)
        # 加载保存的图片
        self.images = {'U': pygame.image.load('img/U.2.png'),
                       'D': pygame.image.load('img/D.2.png'),
                       'L': pygame.image.load('img/L.2.png'),
                       'R': pygame.image.load('img/R.2.png')
                       }
        # 设置敌方坦克方向
        self.direction = self.randDirection()
        # 根据方向获取图片
        self.image = self.images.get(self.direction)
        # 获取矩形区域
        self.rect = self.image.get_rect()
        # 设置left,top
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        # 设置步数
        self.step = 50

    # 设置射击方法
    def shot(self):
        num = random.randint(0, 100)
        if num < 5:
            return bullet(self)

    # 敌方坦克与我方碰撞
    def enemytkhitmytabke(self):

        if pygame.sprite.collide_rect(self, Maingame.mytanke):
            self.stay()

    # 随机生成方向
    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    # 随机移动的方法
    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1

    # 碰撞我方坦克
    def hitmytanke(self):
        pass


# 子弹类
class bullet(BaseItem):
    # 初始化
    def __init__(self, tank):
        # 获取子弹图片
        self.image = pygame.image.load('img/bullet.png')
        # 设置方向
        self.direction = tank.direction
        # 获取子弹图片区域
        self.rect = self.image.get_rect()
        # 设置left,top
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + 4 * self.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - tank.rect.width / 2 + self.rect.width
            self.rect.top = tank.rect.top + 1.5 * self.rect.height
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width / 2 + 2 * self.rect.width
            self.rect.top = tank.rect.top + 1.5 * self.rect.height
        # 子弹速度
        self.speed = 6
        # 是否存活
        self.live = True

    # 移动
    def bulletmove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:  # 碰到墙壁
                self.live = False

        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:  # 碰到墙壁
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:  # 碰到墙壁
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:  # 碰到墙壁
                self.live = False

    # 展示子弹
    def displaybullet(self):
        # 将图片加载到窗口
        Maingame.window.blit(self.image, self.rect)

    # 击中我方坦克
    def hitmytanke(self):
        if Maingame.mytanke and Maingame.mytanke.live:
            if pygame.sprite.collide_rect(self, Maingame.mytanke):
                expl = explode(Maingame.mytanke)
                Maingame.expllist.append(expl)
                self.live = False
                Maingame.mytanke.live = False

    # 击中敌方坦克
    def hitenemytanke(self):
        # 遍历敌方坦克列表
        for enemytanke in Maingame.enemyList:
            if pygame.sprite.collide_rect(self, enemytanke):
                # 修改子弹 和敌坦克状态
                enemytanke.live = False
                self.live = False
                # 初始化爆炸出效果
                expl = explode(enemytanke)
                Maingame.expllist.append(expl)

    # 击中墙壁
    def hitwalls(self):
        for walls in Maingame.wallslist:
            if pygame.sprite.collide_rect(self, walls):
                self.live = False
                walls.hp -= 1
                if walls.hp <= 0:
                    walls.live = False


# 墙壁类
class Walls():
    # 初始化
    def __init__(self, left, top):
        # 加载图片
        self.images = pygame.image.load('img/qb.png')
        # 获取区域
        self.rect = self.images.get_rect()
        # 设置left,top
        self.rect.left = left
        self.rect.top = top
        # 存活状态
        self.live = True
        # 生命值
        self.hp = 6

    # 展示墙壁
    def displaywalls(self):
        Maingame.window.blit(self.images, self.rect)


# 爆炸效果类
class explode():
    # 初始化
    def __init__(self, tanke):
        # 爆炸位置
        self.rect = tanke.rect
        self.images = [
            pygame.image.load('img/02.png'),
            pygame.image.load('img/03.png'),
            pygame.image.load('img/03.png'),
            pygame.image.load('img/03.png'),
            pygame.image.load('img/03.png'),
            pygame.image.load('img/03.png')
        ]
        self.step = 0
        self.image = self.images[self.step]
        # 生存状态
        self.live = True

    # 展示爆炸效果
    def displayexplode(self):
        if self.step < len(self.images):
            self.imsge = self.images[self.step]
            self.step += 1
            # 添加到主窗口
            Maingame.window.blit(self.image, self.rect)
        else:
            self.live = False
            self.step = 0


# 主方法
if __name__ == '__main__':
    # 调用主类中startgame()
    Maingame().sartgame()
