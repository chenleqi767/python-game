# 练习1：定义函数，将列表中0元素，移动到末尾。
# [2,0,2,0]   -->  [2,2,0,0]
# [0,4,2,4]   -->  [4,2,4,0]

# 适合零基础同学
def zero_to_end(list_target):
    # 选出非零元素 形成新列表
    # [2, 0, 2, 0] -->  [2, 2]
    new_list = []
    for item in list_target:
        if item != 0:
            new_list.append(item)
            # 追加零元素 [2, 2] --> [2,2,0,0]
    # 判断原列表零元素数量： list_target.count(0)
    for i in range(list_target.count(0)):
        new_list.append(0)
        # 返回新列表
    return new_list


# def zero_to_end(list_target):
#     # 选出非零元素 形成新列表
#     # [2, 0, 2, 0] -->  [2, 2]
#     new_list = [item for item in list_target if item != 0]
#     # 重复生成零元素 [0] * list_target.count(0)
#     new_list += [0] * list_target.count(0)
#     # 返回新列表
#     return new_list

# 同学方法
# def zero_to_end(list_target):
#     # 删除零元素  在后面追加
#     for item in list_target:
#         if item == 0:
#             list_target.remove(0)
#             list_target.append(item)
#     # 返回新列表
#     return list_target


# 测试
# print(zero_to_end([1, 0, 0, 2]))
# print(zero_to_end([0, 4, 2, 4]))

# 练习2：定义合并相同（不相邻也可以）列表元素的函数
# [2,2,0,0]    -->  [4,0,0,0]
# [2,0,2,0]    -->  [4,0,0,0]
# [2,2,2,0]    -->  [4,2,0,0]
# [4,2,0,4]    -->  [4,2,4,0]
# [0,0,2,4]    -->  [2,4,0,0]
# 提示：
# 0元素移动到末尾
# 相邻相同合并
# list[0] == list[1]

def merge(list_target):
    # 1.将零元素移动到末尾 [2,0,2,0]    -->  [2,2,0,0]
    list_target = zero_to_end(list_target)
    # 2. 合并
    for i in range(len(list_target) - 1):
        # 如果非零元素  相邻且相同
        if list_target[i] != 0 and list_target[i] == list_target[i + 1]:
            # 将后一个元素累加到前一个元素上
            list_target[i] += list_target[i + 1]
            # 讲后一个元素清零
            list_target[i + 1] = 0
    # 3. 将零元素移动到末尾  [2,2,2,0]    -->  [4,0,2,0]  -->[4,2,0,0]
    list_target = zero_to_end(list_target)
    return list_target


# print(merge([2,2,2,0]))

# 练习3:定义在控制台中绘制2048地图的函数 11:33
def print_atlas(list_atlas):
    # 00   01   02   03
    for r in range(len(list_atlas)):
        for c in range(len(list_atlas[r])):
            print(list_atlas[r][c], end=" ")
        print()


atlas01 = [
    [2, 0, 0, 2],
    [8, 0, 4, 4],
    [2, 2, 0, 4],
    [0, 2, 4, 0],
]

print_atlas(atlas01)


# 练习4：在控制台中打印第二行，与第四行元素。
#                   第一列，与第三列元素。
# 第二行
# for c in range(4):
#     print(atlas01[1][c], end=" ")
# print()
# # 第四行
# for c in range(4):
#     print(atlas01[3][c], end=" ")
# print()
# # 第一列
# for r in range(4):
#     print(atlas01[r][0])
# # 第三列
# for r in range(4):
#     print(atlas01[r][2])


# 练习5，定义向上移动的函数
# 提示：将二维列表每列元素形成一维列表,交给合并merge函数,再还给二维列表
def move_up(atlas):  # 15:30
    # 将二维列表第一列元素形成一维列表,
    # 00  10   20  30
    for c in range(4):
        list_merge = []
        for r in range(4):
            list_merge.append(atlas[r][c])

        # 交给合并merge函数
        list_merge = merge(list_merge)

        # 再还给二维列表
        for r in range(4):
            atlas[r][c] = list_merge[r]
    return atlas


# resutl = move_up(atlas01)
# print_atlas(resutl)


# 扩展作业1：定义向左移动的函数
def move_left(atlas):
    for r in range(4):
        # 从左到右依次获取行
        list_merge = []
        for c in range(4):
            # 00  01  02  03
            list_merge.append(atlas[r][c])

        list_merge = merge(list_merge)

        for c in range(4):
            atlas[r][c] = list_merge[c]

    return atlas


# resutl = move_left(atlas01)
# print_atlas(resutl)


# 扩展作业2：定义向下移动的函数
# 30   20   10  00
def move_down(atlas):
    for c in range(4):
        list_merge = []
        # 从下至上获取二维列表列元素
        for r in range(3, -1, -1):
            list_merge.append(atlas[r][c])

        list_merge = merge(list_merge)

        # 从左至右获取一维列表元素
        # 从下至上还给二维列表
        for r in range(3, -1, -1):
            atlas[r][c] = list_merge[3 - r]  # 0  1 2 3
    return atlas


def move_right(atlas):
    for r in range(4):
        list_merge = []
        for c in range(3, -1, -1):
            list_merge.append(atlas[r][c])

        list_merge = merge(list_merge)

        for c in range(3, -1, -1):
            atlas[r][c] = list_merge[3 - c]
    return atlas


# resutl = move_down(atlas01)
# print_atlas(resutl)

# 扩展作业3：定义向右移动的函数
while True:
    shell = input("请输入玩家指令wsad:")
    if shell == "w":
        move_up(atlas01)
        print_atlas(atlas01)
    elif shell == "s":
        move_down(atlas01)
        print_atlas(atlas01)
    elif shell == "a":
        move_left(atlas01)
        print_atlas(atlas01)
    elif shell == "d":
        move_right(atlas01)
        print_atlas(atlas01)
    else:
        print("输入错误")
