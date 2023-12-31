"""
from zifan.site
version 1.1.0
python 3.x
"""
import sys
import random
import time
import numba as nb

from collections import deque
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse
import math

TICKS_PER_SEC = 60

SECTOR_SIZE = 16

GAMETYPES = True # 是否开启冰雪世界

SEED = random.randint(10, 1000000)#656795(种子"akioi") # 世界种子
print('seed:', SEED)

GTIME = 0 # 当前世界时间
GDAY = 0.0005
GNIGHT = 0.0015

WALKING_SPEED = 5 # 走路速度
RUNNING_SPEED = 8 # 跑步速度
FLYING_SPEED = 15 # 飞行速度

GRAVITY = 35.0 # 重力
MAX_JUMP_HEIGHT = 1.25 # 最大跳跃速度
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 35 # 终端速度

PLAYER_HEIGHT = 2 # 玩家高度

WORLDLEN = 128 # 世界长度

TEXTURE_PATH = 'texture.png' # 纹理文件

def cube_vertices(x, y, z, n):
    # 返回立方体的顶点，大小为2n。
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]

def tex_coord(x, y, n=8):
    # 返回纹理的边界顶点。
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    # 返回顶部、底部和侧面的纹理列表。
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

if GAMETYPES:
    GRASS = tex_coords((4, 0), (0, 1), (1, 3))
else:
    GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
DIRT = tex_coords((0, 1), (0, 1), (0, 1))
STONE = tex_coords((2, 0), (2, 0), (2, 0))
ENDSTONE = tex_coords((2, 1), (2, 1), (2, 1))
if GAMETYPES:
    WATER = tex_coords((3, 1), (3, 1), (3, 1))
else:
    WATER = tex_coords((0, 4), (0, 4), (0, 4))
WOOD = tex_coords((0, 2), (0, 2), (3, 0))
LEAF = tex_coords((0, 3), (0, 3), (0, 3))
BRICK = tex_coords((1, 2), (1, 2), (1, 2))
PUMKEY = tex_coords((2, 2), (3, 3), (2, 3))
MELON = tex_coords((2, 4), (2, 4), (1, 4))
CLOUD = tex_coords((3, 2), (3, 2), (3, 2))
TNT = tex_coords((4, 2), (4, 3), (4, 1))

# 立方体的6个面
FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

random.seed(SEED)


def normalize(position):
    # 将三维坐标'position'的x、y、z取近似值
    x, y, z = position
    x, y, z = (round(x), round(y), round(z))
    return (x, y, z)


def sectorize(position):
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)


persistence = random.uniform(0.01, 0.15)
Number_Of_Octaves = random.randint(3, 5)

@nb.jit(nopython=True, fastmath=True)
def Noise(x, y):
    n = x + y * 57
    n = (n * 8192) ^ n
    return ( 1.0 - ( (n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

@nb.jit(nopython=True, fastmath=True)
def SmoothedNoise(x, y):
    corners = ( Noise(x-1, y-1)+Noise(x+1, y-1)+Noise(x-1, y+1)+Noise(x+1, y+1) ) / 16
    sides = ( Noise(x-1, y) +Noise(x+1, y) +Noise(x, y-1) +Noise(x, y+1) ) / 8
    center = Noise(x, y) / 4
    return corners + sides + center

@nb.jit(nopython=True, fastmath=True)
def Cosine_Interpolate(a, b, x):
    ft = x * 3.1415927
    f = (1 - math.cos(ft)) * 0.5
    return a*(1-f) + b*f

@nb.jit(nopython=True, fastmath=True)
def Linear_Interpolate(a, b, x):
    return a*(1-x) + b*x

def InterpolatedNoise(x, y):
    integer_X = int(x)
    fractional_X = x - integer_X
    integer_Y = int(y)
    fractional_Y = y - integer_Y
    v1 = SmoothedNoise(integer_X, integer_Y)
    v2 = SmoothedNoise(integer_X + 1, integer_Y)
    v3 = SmoothedNoise(integer_X, integer_Y + 1)
    v4 = SmoothedNoise(integer_X + 1, integer_Y + 1)
    i1 = Cosine_Interpolate(v1, v2, fractional_X)
    i2 = Cosine_Interpolate(v3, v4, fractional_X)
    return Cosine_Interpolate(i1, i2, fractional_Y)

def PerlinNoise(x, y):
    noise = 0
    p = persistence
    n = Number_Of_Octaves
    for i in range(n):
        frequency = pow(2,i)
        amplitude = pow(p,i)
        noise = noise + InterpolatedNoise(x * frequency, y * frequency) * amplitude
    return noise

class Model(object):

    def __init__(self):

        self.batch = pyglet.graphics.Batch()
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture()) # 纹理列表
        self.world = {} # 地图
        self.shown = {} # 显示的方块
        self._shown = {} # 显示的纹理
        self.sectors = {}
        self.queue = deque()
        self.dfy = self._initialize()

    def tree(self, y, x, z):
        # 生成树
        th = random.randint(4, 6)
        ts = random.randint(th // 2, 4)
        for i in range(y, y + th):
            self.add_block((x, i, z), WOOD, immediate=False)
        for dy in range(y + th, y + th + 2):
             for dx in range(x - ts, x + ts + 1):
                for dz in range(z - ts, z + ts + 1):
                    self.add_block((dx, dy, dz), LEAF, immediate=False)
        for dy in range(y + th + 2, y + th + ts + 2):
            ts -= 1
            for dx in range(x - ts, x + ts + 1):
                for dz in range(z - ts, z + ts + 1):
                    self.add_block((dx, dy, dz), LEAF, immediate=False)

    def _initialize(self):
        # 初始化世界
        hl = WORLDLEN // 2
        mn = 0
        quality = 4
        gmap = [[0 for x in range(0, WORLDLEN)]for z in range(0, WORLDLEN)]
        for x in range(0, WORLDLEN):
            for z in range(0, WORLDLEN):
                gmap[x - hl][z - hl] += round(PerlinNoise(x / quality, z / quality) * quality)
                mn = min(mn, gmap[x - hl][z - hl])
        for x in range(-hl, hl):
            for z in range(-hl, hl):
                gmap[x][z] += abs(mn)
                if gmap[x][z] < 2:
                    self.add_block((x, -1, z), random.choice([SAND, STONE]))
                    self.add_block((x, 0, z), WATER)
                    if GAMETYPES:
                        self.add_block((x, 1, z), WATER)
                    else:
                        self._show_block((x, 1, z), WATER)
                else:
                    for y in range(-1, gmap[x][z]):
                        self.add_block((x, y, z), DIRT)
                    self.add_block((x, gmap[x][z], z), GRASS)
                self.add_block((x, -2, z), ENDSTONE)
        for x in range(-hl, hl, 4):
            for z in range(-hl, hl, 4):
                if x == 0 and z == 0:
                    continue
                if random.randint(0, 3) == 1 and gmap[x][z] > 1:
                    self.tree(gmap[x][z] + 1, x, z)
                    for i in range(x, x + 4):
                        for j in range(z, z + 4):
                            self._show_block((i, 30, j), CLOUD)
                elif random.randint(0, 4) == 2 and gmap[x][z] > 2:
                    self.add_block((x, gmap[x][z] + 1, z), random.choice([PUMKEY, MELON]))
        return gmap[0][0] + abs(mn) + 2

    def hit_test(self, position, vector, max_distance=8):
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def exposed(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False

    def add_block(self, position, texture, immediate=True):
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def remove_block(self, position, immediate=True):
        del self.world[position]
        self.sectors[sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def check_neighbors(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)

    def show_block(self, position, immediate=True):
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)

    def _show_block(self, position, texture):
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))

    def hide_block(self, position, immediate=True):
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def _hide_block(self, position):
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dy in [0]:
                for dz in range(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def _enqueue(self, func, *args):
        self.queue.append((func, args))

    def _dequeue(self):
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()

    def process_entire_queue(self):
        while self.queue:
            self._dequeue()


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.exclusive = False
        self.flying = False # 是否在飞行
        self.walking = True # 是否在走路
        self.jumping = False # 是否在跳
        self.model = Model()
        self.strafe = [0, 0]
        self.position = (0, self.model.dfy, 0)
        self.rotation = (0, 0)
        self.sector = None
        self.reticle = None
        self.dy = 0
        self.inventory = [GRASS, DIRT, STONE, SAND, WOOD, BRICK, PUMKEY, MELON, TNT]
        self.block = self.inventory[0]
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)

    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        x, y = self.rotation
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    dy *= -1
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)

    def update(self, dt):
        # 刷新
        global GTIME
        global GNIGHT
        global GDAY
        glClearColor(0.5 - GTIME * 0.01, 0.69 - GTIME * 0.01, 1.0 - GTIME * 0.01, 1)
        setup_fog()
        GTIME += GDAY if GTIME < 23 else GNIGHT
        if GTIME > 50:
            GTIME = 50
            GNIGHT = -GNIGHT
            GDAY = -GDAY
        elif GTIME < 0:
            GTIME = 0
            GNIGHT = -GNIGHT
            GDAY = -GDAY
        self.model.process_queue()
        sector = sectorize(self.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        if self.jumping:
            if self.dy == 0:
                self.dy = JUMP_SPEED
        for _ in range(m):
            self._update(dt / m)

    def _update(self, dt):
        speed = FLYING_SPEED if self.flying else WALKING_SPEED if self.walking else RUNNING_SPEED
        d = dt * speed
        dx, dy, dz = self.get_motion_vector()
        dx, dy, dz = dx * d, dy * d, dz * d
        if not self.flying:
            self.dy -= dt * GRAVITY
            self.dy = max(self.dy, -TERMINAL_VELOCITY)
            dy += self.dy * dt
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
        self.position = (x, y, z)

    def collide(self, position, height):
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:
            for i in range(3):
                if not face[i]:
                    continue
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(height):
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        self.dy = 0
                    break
        return tuple(p)

    def TNTboom(self, x, y, z):
        # TNT爆炸
        self.model.remove_block((x, y, z))
        bf = 4
        s = 0
        for dy in range(y - bf, y):
            for i in range(x - s, x + s):
                for j in range(z - s, z + s):
                    if (i, dy, j) in self.model.world:
                        if j == z-s or j == z+s-1 or i == x-s or i == x+s-1:
                            if random.randint(0, 1):
                                if self.model.world[(i, dy, j)] == TNT:
                                    self.TNTboom(i, dy, j)
                                    continue
                                if self.model.world[(i, dy, j)] != ENDSTONE:
                                    self.model.remove_block((i, dy, j))
                        else:
                            if self.model.world[(i, dy, j)] == TNT:
                                self.TNTboom(i, dy, j)
                                continue
                            if self.model.world[(i, dy, j)] != ENDSTONE:
                                self.model.remove_block((i, dy, j))
            s += 1
        s = bf
        for i in range(x - s, x + s):
            for j in range(z - s, z + s):
                if (i, y, j) in self.model.world:
                    if j == z-s or j == z+s-1 or i == x-s or i == x+s-1:
                        if random.randint(0, 1):
                            if self.model.world[(i, y, j)] == TNT:
                                self.TNTboom(i, y, j)
                                continue
                            self.model.remove_block((i, y, j))
                    else:
                        if self.model.world[(i, y, j)] == TNT:
                            self.TNTboom(i, y, j)
                            continue
                        self.model.remove_block((i, y, j))
        for dy in range(y + 1, y + s + 1):
            for i in range(x - s, x + s):
                for j in range(z - s, z + s):
                    if (i, dy, j) in self.model.world:
                        if j == z-s or j == z+s-1 or i == x-s or i == x+s-1:
                            if random.randint(0, 1):
                                if self.model.world[(i, dy, j)] == TNT:
                                    self.TNTboom(i, dy, j)
                                    continue
                                if self.model.world[(i, dy, j)] != ENDSTONE:
                                    self.model.remove_block((i, dy, j))
                        else:
                            if self.model.world[(i, dy, j)] == TNT:
                                self.TNTboom(i, dy, j)
                                continue
                            if self.model.world[(i, dy, j)] != ENDSTONE:
                                self.model.remove_block((i, dy, j))
            s -= 1

    def on_mouse_press(self, x, y, button, modifiers):
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous = self.model.hit_test(self.position, vector)
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                if previous:
                    # 鼠标右击
                    x, y, z = self.position
                    flag = True
                    for i in range(0, PLAYER_HEIGHT):
                        if previous == normalize((x, y - i, z)):
                            flag = False
                            break
                    if flag:
                        self.model.add_block(previous, self.block)
            elif button == pyglet.window.mouse.LEFT and block:
                # 鼠标左击
                texture = self.model.world[block]
                if texture == TNT:
                    self.TNTboom(block[0], block[1], block[2])
                elif texture != ENDSTONE:
                    self.model.remove_block(block)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        # 键盘按键
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            self.jumping = True
        elif symbol == key.R:
            self.walking = not self.walking
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.E:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]

    def on_key_release(self, symbol, modifiers):
        # 键盘松键
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
        elif symbol == key.SPACE:
            self.jumping = False

    def on_resize(self, width, height):
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def set_2d(self):
        # 3d模式
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        # 3d模式
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        # 绘制
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.draw_focused_block()
        self.set_2d()
        self.draw_label()
        self.draw_reticle()

    def draw_focused_block(self):
        vector = self.get_sight_vector()
        block = self.model.hit_test(self.position, vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        x, y, z = self.position
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z,
            len(self.model._shown), len(self.model.world))
        self.label.draw()

    def draw_reticle(self):
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)


def setup_fog():
    # 初始化迷雾和光照
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5 - GTIME * 0.01, 0.69 - GTIME * 0.01, 1.0 - GTIME * 0.01, 1))
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 30.0)
    glFogf(GL_FOG_END, 60.0)
    glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(0.0, 0.0, 0.0, 0.0))
    setup_light()

def setup_light():
    # 初始化光照
    gamelight = 5.0 - GTIME / 10
    glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat * 4)(gamelight, gamelight, gamelight, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat * 4)(gamelight, gamelight, gamelight, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat * 4)(1.0, 1.0, 1.0, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def setup():
    # 初始化
    glClearColor(0.5 - GTIME * 0.01, 0.69 - GTIME * 0.01, 1.0 - GTIME * 0.01, 1)
    glEnable(GL_CULL_FACE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    setup_fog()

def main():
    window = Window(width=800, height=600, caption='Python Minecraft', resizable=True)
    window.set_exclusive_mouse(True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()
