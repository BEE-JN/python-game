import random
import math
import pygame
from pygame.locals import *

# 创建游戏
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
# 设置箭
arrows = []
# 记录键盘WASD的按键
keys = [False, False, False, False]  # 0代表w，1代表a，2代表s，3代表d
# playerpos表示玩家的位置
playerpos = [100, 100]
# 初始化坏蛋
badtimer = 100
badtimer1 = 0
badguys = [[640, 100, 1]]  # 二维列表，表示坏蛋出现的位置，初始情况下坏蛋只出现一个
healthvalue = 194

# 加载控制对象图片
player = pygame.image.load("resources\images\dude2.png")
# 增加背景
background = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
# 增加弓箭图标
arrow = pygame.image.load("resources/images/bullet.png")
# 坏蛋出现
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg = badguyimg1
# 创建血量条
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

running = 1
exitcode = 0
# 重复
while running:  # while 1是用来干什么的？
    # 清屏
    screen.fill(0)
    # 将控制对象放在屏幕上
    # 让背景覆盖整个窗口
    for x in range(width // background.get_width() + 1):
        for y in range(height // background.get_height() + 1):
            screen.blit(background, (x * 100, y * 100))
    # 放置城堡
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))
    # 玩家转身
    # 首先获得兔子的位置
    position = pygame.mouse.get_pos()
    # 计算玩家偏转角度
    angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
    # 函数是逆时针旋转？
    playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
    # 获得玩家旋转之后的位置
    playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
    # 显示玩家位置
    screen.blit(playerrot, playerpos1)
    # 玩家点击一次鼠标射一只箭
    for bullet in arrows:  # bullet是arrows中的元素
        index = 0
        velx = math.cos(bullet[0]) * 10     #箭的速度
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index += 1
        for projextile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projextile[0] * 57.29)
            screen.blit(arrow1, (projextile[1], projextile[2]))
    # 判断badtimer是否为0，若为0则创建一个坏蛋
    badtimer -= 1
    if badtimer == 0:
        badguys.append([640, random.randint(50, 430), random.randint(1,2)])  # 随机坏蛋出现的位置（y轴）
        badtimer = 100 - (badtimer1 * 2)  # 坏蛋出现的越来越频繁
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    index = 0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)  # 若第一个元素的【0】>-64，则该元素移动3格，index++，判断badguys列表中的第二个元素中的【0】是否<-64
        badguy[0] -= 3  #badguy的速度
        # 判断坏蛋攻击到了城堡
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            healthvalue -= random.randint(5, 18)  # 随机每次的伤害量
            badguys.pop(index)  # 坏蛋攻击城堡后删除
        # 判断箭头是否击中坏蛋
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                badguy[2]-=1
                if badguy[2] == 0:
                    badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        index += 1
    # 如果有badguy就显示出来
    for badguy in badguys:
        screen.blit(badguyimg, (badguy[0],badguy[1]))  # 若badguys中有元素，则显示，badguy为元素，本身也是列表，表示坐标
    # 设置一个计时器记录存活时间
    font = pygame.font.SysFont("Arial",30)
    survivedtext = font.render("COUNTDOWN: " +
        str((25000 - pygame.time.get_ticks()) // 60000) + ":" + str(
            (25000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2), True, (0, 0, 0))
    # pygame.time.get_ticks()
    # Return the number of milliseconds since pygame.init() was called.
    # Before pygame is initialized this will always be 0.
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)
    # 画出血量
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8, 8))
    # 刷新屏幕
    pygame.display.flip()

    # 检查事件
    for event in pygame.event.get():
        # 检查是否是关闭
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        # 控制玩家的移动
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_s:  # 使用elif则4个键只能识别一个
                keys[2] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_d:
                keys[3] = True
            if event.key == K_f:        #按F可以全屏，在按一次可以退出全屏
                FULLSCREEN = not FULLSCREEN
                if FULLSCREEN:
                    screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((width,height))
            if event.key == K_o:
                pygame.quit()
                exit(0)
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_d:
                keys[3] = False
        # 玩家点击一次鼠标射一只箭
        if event.type == pygame.MOUSEBUTTONDOWN:
            #position = pygame.mouse.get_pos()
            arrows.append(
                [math.atan2(position[1] - (playerpos1[1] + 32 ), position[0] - (playerpos1[0] + 26 )), playerpos1[0] + 32,
                 playerpos1[1] + 32])
    # 根据按键更改玩家位置
    if keys[0]:  # W
        if playerpos[1] >= 5:
            playerpos[1] -= 5  # w和s只能识别一个，通过利用if''''elif语句
    elif keys[2]:  # S
        if playerpos[1] <= 475:
            playerpos[1] += 5
    if keys[1]:  # A
        if playerpos[0] >= 5:
            playerpos[0] -= 5
    elif keys[3]:  # D
        if playerpos[0] <= 635:
            playerpos[0] += 5
    # 将新的位置当做初始位置
    # screen.blit(player, playerpos)  #这句话用来干啥的？

    # 失败后操作
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    # 胜利后操作
    if pygame.time.get_ticks() >= 25000:
        running = 0
        exitcode = 1
# 判断成功或者失败
if exitcode == 0:
    screen.blit(gameover, (0, 0))
if exitcode == 1:
    screen.blit(youwin, (0, 0))
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit(0)
        if event.type == KEYDOWN:
            if event.key == K_f:        #按F可以全屏，在按一次可以退出全屏
                FULLSCREEN = not FULLSCREEN
                if FULLSCREEN:
                    screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((width,height))
    pygame.display.flip()
