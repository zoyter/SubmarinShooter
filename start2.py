#-*- coding: utf-8 -*-
import random as rnd
import pygame as pyg
from pygame.locals import *

pyg.init()
size = [800,600]
screen = pyg.display.set_mode(size)
clock = pyg.time.Clock()
isGame = True

font = pyg.font.Font("Ru.ttf", 40)  

# Загружаем картинки
bg = pyg.image.load('fon.png').convert_alpha()
#bg = pyg.image.load('The Hunt for Red October 1.jpg').convert()
#bg = pyg.transform.scale(bg,(800,600))

h_img = pyg.image.load('hero.png').convert_alpha()
h_img = pyg.transform.scale(h_img,(50,50))
#h_img = pyg.transform.scale(h_img,(200,50))

e_img = pyg.image.load('enemy.png').convert_alpha()
e_img = pyg.transform.scale(e_img,(200,100))

e2_img = pyg.image.load('enemy1.png').convert_alpha()
e2_img = pyg.transform.scale(e2_img,(200,100))
e2_img = pyg.transform.rotate(e2_img,0)


bo1_img = pyg.image.load('cloud.png').convert_alpha()
bo1_img = pyg.transform.scale(bo1_img,(100,100))

anim1 = []
x=pyg.image.load('bird1.png').convert_alpha()
x=pyg.transform.scale(x,(50,50))
anim1.append(x)
x=pyg.image.load('bird2.png').convert_alpha()
x=pyg.transform.scale(x,(50,50))
anim1.append(x)


torpeda_img = pyg.image.load('torpeda.png').convert_alpha()
torpeda_img = pyg.transform.scale(torpeda_img,(320//10,640//10))

boom_img = pyg.image.load('boom.png').convert_alpha()
#boom_img = pyg.transform.scale(boom_img,(320//10,640//10))


frame = 10
frame_max = 10
frame_cur = 0


#Координаты
h_x = 100
h_y = 400
h_xs = 10
h_ys = 10

e_x = 200
e_y = 100
e_xs = 5
e_ys = 10
e_boom = False

e2_x = 100
e2_y = 130
e2_xs = 3
e2_ys = 10
e2_boom = False

bo1_x = 200
bo1_y = 50
bo1_xs = 3
bo1_ys = 10

anim1_x = 50
anim1_y = 50
anim1_xs = 5

anim1_x = 50
anim1_y = 50
anim1_xs = 5
anim1_ys = 5

anim2_x = 150
anim2_y = 50
anim2_xs = 1
anim2_ys = 1



torpeda_x = 150
torpeda_y = 50
torpeda_xs = 2
torpeda_ys = 2


isBoom = False
boom_time = 100
boom_max_time = 100

torpeda_flag = False


b_left = False
b_right = False

state = 0

def title():
    global bo1_x, frame_cur, frame, anim1_x, anim2_x,anim2_y, anim2_xs, anim2_ys, torpeda_x, torpeda_y, torpeda_xs, torpeda_ys
    print("Идет заставка")
    screen.blit(bg,[0,0])

    t = "The Hunt for Red october"
    text_color = (255,0,0)
    text = font.render(t,True,text_color)
    x = screen.get_width() // 2 - text.get_width() // 2
    y = screen.get_height() // 2 - text.get_height() // 2
    # отрисовываем текст
    screen.blit(text,[x,y])
    bo1_x += bo1_xs
    if bo1_x >= 800:
        bo1_x = 0 - bo1_img.get_width()
    screen.blit(bo1_img,[bo1_x,bo1_y])

    frame -= 1
    if frame <=0:
        frame_cur += 1
        # Вот тут какая-то ерунда
        if frame_cur > len(anim1)-1:
            frame_cur = 0
        #---------------------
        frame = frame_max
    anim1_x += anim1_xs
    if anim1_x > 800:
        anim1_x = 0 - anim1[0].get_width()
    screen.blit(anim1[frame_cur],[anim1_x,anim1_y])

    anim2_x += anim2_xs
    anim2_y += anim2_ys
    if anim2_x<=0 or anim2_x + anim1[0].get_width() >=800:
        anim2_xs = -anim2_xs
    if anim2_y<=0 or anim2_y + anim1[0].get_height() >=150:
        anim2_ys = -anim2_ys        
    screen.blit(anim1[frame_cur],[anim2_x,anim2_y])

    torpeda_y -= torpeda_ys
    if torpeda_y + torpeda_img.get_height() <=0:
        torpeda_y = 600
        torpeda_x = rnd.randint(0,800-torpeda_img.get_width())
    screen.blit(torpeda_img,[torpeda_x,torpeda_y])    
    
    
def game():
    global h_x, h_y, e_x, e_y, e2_x, e2_y, torpeda_x, torpeda_y, torpeda_xs, torpeda_ys, torpeda_flag, e_boom, e2_boom
    #print("Идет игра")
    #Действия
    if b_left == True:
        h_x -= h_xs
        if h_x <=0:
            h_x = 0
    if b_right == True:
        h_x += h_xs
        if h_x >= 800:
            h_x = 800

    e_x += e_xs
    if e_x >= 800:
        e_x = 0 - e_img.get_width()
        e_boom = False

    e2_x -= e2_xs
    if e2_x <= 0 - e2_img.get_width():
        e2_x = 800
        
    #Рисование
    screen.blit(bg,[0,0])

    screen.blit(h_img,[h_x,h_y])
    if e_boom == True:
        #screen.blit(e_img,[e_x,e_y])
        screen.blit(boom_img,[e_x,e_y])
    else:
        screen.blit(e_img,[e_x,e_y])
        
    screen.blit(h_img,[h_x,h_y])
    if e2_boom == True:
        #screen.blit(e_img,[e_x,e_y])
        screen.blit(boom_img,[e2_x,e2_y])
    else:
        screen.blit(e2_img,[e2_x,e2_y])

    #Выстрел
    if torpeda_flag == True:
        torpeda_y -= torpeda_ys
        if torpeda_y + torpeda_img.get_height() <=0:
            torpeda_flag = False

        torpeda_c = torpeda_x + torpeda_img.get_width() // 2
        xb = torpeda_c > e_x and torpeda_c < e_x + e_img.get_width()
        yb = torpeda_y < e_y + e_img.get_height()  and torpeda_y > e_y

        pyg.draw.line(screen, (255,0,0), (0, torpeda_y), (800, torpeda_y),5)
        pyg.draw.line(screen, (255,0,0), (torpeda_c, 0), (torpeda_c, 800),5)
        
        pyg.draw.line(screen, (0,255,0), (0, e_y+e_img.get_height()), (800, e_y+e_img.get_height()), 5)
        pyg.draw.line(screen, (0,255,0), (0, e_y), (800, e_y), 5)
        pyg.draw.line(screen, (0,255,0), (e_x, 0), (e_x, 600), 5)
        pyg.draw.line(screen, (0,255,0), (e_x+e_img.get_width(), 0), (e_x+e_img.get_width(), 600), 5)                        

        if xb and yb:
            e_boom = True
            pyg.draw.rect(screen, (0,0,255), (e_x, e_y, e_img.get_width(), e_img.get_height()),0)
        else:
            screen.blit(torpeda_img,[torpeda_x,torpeda_y])
        
    #

def gameover():
    print("игра завершена")

def win():
    print("Победа")

def pause():
    print("Пауза")

while isGame:
    #События
    for e in pyg.event.get():
        if e.type == QUIT:
                isGame = False
        if e.type == KEYDOWN:
            if state == 0:
                state = 1
            if e.key == K_ESCAPE:
                isGame = False
            if e.key == K_LEFT:
                b_left = True
                b_right = False
            if e.key == K_RIGHT:
                b_right = True
                b_left = False
            if e.key == K_p:
                state = 4
            if e.key == K_SPACE:
                if torpeda_flag == False:
                    torpeda_flag = True
                    torpeda_x = h_x
                    torpeda_y = h_y
                
        if e.type == KEYUP:
            if e.key == K_LEFT:
                b_left = False
            if e.key == K_RIGHT:
                b_right = False
    
    if state == 0:
        title()
    elif state == 1:
        game()
    elif state == 2:
        win()
    elif state == 3:
        gameover()
    elif state == 4:
        gameover()
        
    #Отображение
    pyg.display.flip()
    #Пауза
    clock.tick(60)
pyg.quit()
quit()
