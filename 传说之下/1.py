from arcade import *
from sys import exit
import random
import math
import time
import colorsys as color
LEFT = 65361     # 向左方向箭头按键码
UP = 65362       # 向上方向箭头按键码
RIGHT = 65363    # 向右方向箭头按键码
DOWN = 65364
PRE_ATTACK=1
ATTACK=2

#龙炮弹类
class dragon(Sprite):
    def __init__(self,filename,px,py):
        super().__init__(filename)
        #初始化
        self.center_x=random.choice((random.randint(0,20),random.randint(780,800)))
        self.center_y = random.choice(
            (random.randint(0, 20), random.randint(580, 600)))
        self.angle = math.degrees(math.atan((px-self.center_x)/(py-self.center_y)))
        self.append_texture(load_texture('dragon.jpg',scale=2))
        self.append_texture(load_texture('dragon2.jpg',scale=5))

        self.set_texture(PRE_ATTACK)
        self.time=0
        schedule(self.timer,1)
        self.mode=PRE_ATTACK
        #加载音效
        self.shoot=load_sound('shoot.wav')
    def timer(self,a):
        self.time+=1
    #绘制
    def draw(self):
        super().draw()
        if self.time==1:
            self.set_texture(ATTACK)
            play_sound(self.shoot)
            self.mode=ATTACK

#子弹类
class bullets():
    def __init__(self,x,y,speed1,speed2):
        self.x=x
        self.y=y
        self.xspeed=speed1
        self.yspeed=speed2
        self.size=random.randint(30,100)
    def update(self):
        self.x+=self.xspeed
        self.y+=self.yspeed
    def draw(self):
        draw_rectangle_filled(self.x,self.y,self.size,self.size,color=color.RED)
#回血类
class heal():
    def __init__(self,a):

        self.x = random.randint(0,800)
        self.y = random.randint(0,600)
        self.xspeed = random.randint(-4,10)
        self.yspeed = random.randint(-4,10)
        self.size = random.randint(10, 30)

    def update(self):

        self.x += self.xspeed
        self.y += self.yspeed

    def draw(self):
        draw_rectangle_filled(self.x,self.y,self.size,self.size,color=color.GREEN)
#游戏类
class game(Window):
    def __init__(self,width,height,title):
        self.heals=[]#print(width)
        super().__init__(width,height,title)
        self.setup()

    def print_len(self,a):
        print(len(self.bullets))
    #改变sans坐标
    def xy(self,a):
        self.pos2=[random.randint(0,self.size[0]),random.randint(0,self.size[1])]
    def print_hp(self,a):
        print(self.hp)
    #回血
    def heal_(self,b):
        self.hp+=1
    def time_(self,a):
        self.second+=1
    #生成治疗
    def heal(self,a):

        self._heal=heal(a)
        self._heal=None

        self._heal=heal(a)

    #生成龙炮弹
    def dragon(self,a):
        self.dragons.append(dragon('dragon.jpg',self.pos[0],self.pos[1]))
    #设置
    def setup(self):

        #全屏
        self.set_fullscreen(True)
        #屏幕大小
        self.size=self.get_size()
        ##加载治疗音效
        self.heal_sound=load_sound('heal.wav')

        self.second=0
        schedule(self.time_,1)
        self.heal('none')
        #龙精灵组
        self.dragons=SpriteList()
        schedule(self.shoot_bullet,0.3)
        self.hp=100
        self.hp2=100
        self.pos=[100,100]
        self.pos2=[500,100]
        self.attack=False
        self.bullets=[]
        self.xspeed=0
        self.yspeed=0
        self.san_2=Sprite('sans2.jpg')
        self.san_2.center_x=400
        self.san_2.center_y=300
        self.is_end=False
        #schedule(self.print_len,4)
        schedule(self.xy,3)
        #schedule(self.print_hp,5)
        #图片，声音
        self.heart=Sprite('heart.jpg')
        self.heart.center_x=self.size[0]-200
        self.heart.center_y=self.size[1]-100
        self.hurt=load_sound('attack.wav')
        self.sans=Sprite('sans.jpg')
        self.sans.center_x=self.pos2[0]
        self.sans.center_y=self.pos2[1]
        self.player = Sprite('heart.jpg')
        self.player.center_x = self.pos[0]
        self.player.center_y = self.pos[1]

        schedule(self.dragon,5)
    #绘制各角色
    def on_draw(self):
        start_render()
        set_background_color(color.BLACK)
        draw_rectangle_filled(400,300,800,600,color=color.BLACK)
        #draw_rectangle_filled(self.pos[0],self.pos[1],30,30,color=color.BLUE)
        draw_rectangle_filled(
            self.pos2[0], self.pos2[1], 10, 10, color=color.RED)
        for _bullet in self.bullets:
            _bullet.draw()
        self.heart.draw()
        draw_text('x'+str(self.hp),self.size[0]-150,self.size[1]-100,color.WHITE,50)
        self.sans.draw()
        self.player.draw()
        for _heal in self.heals:
            _heal.draw()
        self._heal.draw()
        if self.is_end:
            self.san_2.draw()
        #绘制龙炮弹
        for d in self.dragons:
            d.draw()
            if d.time>=6:
                self.dragons.remove(d)
    #发射按钮函数
    def shoot_bullet(self,none):

        l1=[a for a in range(1,20)]
        l2 =[a for a in range(-1, -20, -1)]
        l1=l1+l2
        #print(random.choice(l1))
        self.bullets.append(
            bullets(self.pos2[0], self.pos2[1], random.choice(l1), random.choice(l1)))
    #逻辑和按钮
    def on_update(self,delta_time):


        self.sans.center_x = self.pos2[0]
        self.sans.center_y = self.pos2[1]
        self.player.center_x = self.pos[0]
        self.player.center_y = self.pos[1]
        if self.attack:
            self.bullets.append(bullets(self.pos[0],self.pos[1],10,0))
            self.attack=False
        for _bullet in self.bullets:
            _bullet.update()
            if _bullet.x>self.size[0] or _bullet.x<0 or _bullet.y>self.size[1] or _bullet.y<0:
                self.bullets.remove(_bullet)
        self.pos[0]+=self.xspeed
        self.pos[1]+=self.yspeed
        for _heal in self.heals:
            _heal.update()
        #传送回00
        if self.pos[0]<0 or self.pos[0]>self.size[0] or self.pos[1]<0 or self.pos[1]>self.size[1]:
            self.pos[0],self.pos[1]=400,300
        #判断碰撞
        for _bullet in self.bullets:
            dis=math.hypot(_bullet.x-self.pos[0],_bullet.y-self.pos[1])
            if dis<=_bullet.size:
                self.hp-=1
                play_sound(self.hurt)
        if self.hp<=0:
            print('you died!!')
            print('if there are any bugs,please tell 2DS雷神索尔.')
            print('the end-------')
            exit()
        #更新治疗
        self._heal.update()
        dis=math.hypot(self.pos[0]-self._heal.x,self.pos[1]-self._heal.y)
        if dis<=self._heal.size:
            self._heal.x=100000000000
            schedule(self.heal_,1)
            play_sound(self.heal_sound)
        #判断输赢

        if self.second>=100:
            self.set_fullscreen(False)
            print('you win!!!!')
            self.is_end=True
            self.on_draw()
            self.on_draw()
            print('sans:well......I just want to be your friend.....')
            time.sleep(1)
            print('sans:please!!!!merci me!!!!')
            time.sleep(1)
            answer=input('y/n?')
            if answer=='y':
                print('you:Of course I will sans!We"re friends now！')
                exit()
            else:
                print('sans:you will never,never defeat me!')
                print('I am gonna use my"special" attack!!')
                time.sleep(10000)
        #判断龙炮弹碰撞
        for d in list(self.dragons):
            hit=check_for_collision(self.heart,d)


            if hit:
                self.hp-=1




    #移动
    def on_key_release(self,symbol,modifiers):
        if symbol==65307:#ESC键
            self.attack=True
        if symbol==UP or symbol==DOWN:
            self.yspeed=0
        if symbol==LEFT or symbol==RIGHT:
            self.xspeed=0
    def on_key_press(self,symbol,modifiers):
        if symbol==UP:
            self.yspeed=20
        if symbol==DOWN:
            self.yspeed=-20
        if symbol==LEFT:
            self.xspeed=-20
        if symbol==RIGHT:
            self.xspeed=20
g=game(800,600,'传说之下 v.1.1.5 版权由2DS雷神索尔所有，请勿抄袭')
run()