#-*- coding: utf-8 -*-

# Загрузка модулей
import random as rnd
import pygame as pyg
from pygame.locals import *

#Инициализация pygame
pyg.init()
#Размеры окна
size = [800,600]
#Создаем окно
screen = pyg.display.set_mode(size)
#Создаем таймер
clock = pyg.time.Clock()
#Поднимаем флаг того, что идет игра
isGame = True
#Создаем шрифт для крупных надписей
font = pyg.font.Font("Ru.ttf", 40)
font1 = pyg.font.Font("Ru.ttf", 20)  

####### Загружаем картинки
#Фоновая картинка
bg = pyg.image.load('fon.png').convert_alpha()
#bg = pyg.transform.scale(bg,(800,600))

#Картинка персонажа
h_img = pyg.image.load('hero.png').convert_alpha()
h_img = pyg.transform.scale(h_img,(50,50))
#h_img = pyg.transform.scale(h_img,(200,50))
#Картинка 1-го противника
e_img = pyg.image.load('enemy.png').convert_alpha()
e_img = pyg.transform.scale(e_img,(200,100))
#Картинка 2-го противника
e2_img = pyg.image.load('enemy1.png').convert_alpha()
e2_img = pyg.transform.scale(e2_img,(200,100))

#Облако
bo1_img = pyg.image.load('cloud.png').convert_alpha()
bo1_img = pyg.transform.scale(bo1_img,(100,100))

#Анимация птицы
anim1 = []
x=pyg.image.load('bird1.png').convert_alpha()
x=pyg.transform.scale(x,(50,50))
anim1.append(x)
x=pyg.image.load('bird2.png').convert_alpha()
x=pyg.transform.scale(x,(50,50))
anim1.append(x)

#Анимация аквалангиста
anim3 = []
for i in range(1,9):
    x=pyg.image.load('man%s.png'%(i)).convert_alpha()
    x=pyg.transform.scale(x,(x.get_width() //5 ,x.get_height() //5))
    anim3.append(x)

#Торпеда
torpeda_img = pyg.image.load('torpeda.png').convert_alpha()
torpeda_img = pyg.transform.scale(torpeda_img,(320//10,640//10))

#Взрыв
boom_img = pyg.image.load('boom.png').convert_alpha()

#Счетчики для анимации птицы
frame = 10
frame_max = 10
frame_cur = 0

#Счетчики для анимации аквалангиста
frame3 = 10
frame_max3 = 10
frame_cur3 = 0

#Максимальное время взрыва
boom_max_time = 50

#Координаты персонажа
h_x = 100
h_y = 400
h_xs = 10
h_ys = 10
h_score = 0
h_score_next_level = 1000
h_level = 1
h_hp = 100

e_x = 200
e_y = 100
e_xs = 5
e_ys = 10
e_boom = False
e_boom_time = boom_max_time

e2_x = 100
e2_y = 130
e2_xs = 3
e2_ys = 10
e2_boom = False
e2_boom_time = boom_max_time

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


anim3_x = 50
anim3_y = 250
anim3_xs = 1
anim3_ys = 1

torpeda_x = 150
torpeda_y = 50
torpeda_xs = 2
torpeda_ys = 15




torpeda_flag = False


b_left = False
b_right = False

state = 0


fire = pyg.mixer.Sound('torpeda.wav')
fire2 = pyg.mixer.Sound('fire.wav')
#music = pyg.mixer.Sound('music.mp3')
pyg.mixer.music.load('music.mp3')
pyg.mixer.music.play()


def title():
    global bo1_x, frame_cur, frame, anim1_x, anim2_x,anim2_y, anim2_xs, anim2_ys, torpeda_x, torpeda_y, torpeda_xs, torpeda_ys
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

    draw_bg_anim()
    
    torpeda_y -= torpeda_ys
    if torpeda_y + torpeda_img.get_height() <=0:
        torpeda_y = 600
        torpeda_x = rnd.randint(0,800-torpeda_img.get_width())
    screen.blit(torpeda_img,[torpeda_x,torpeda_y])    
    
    
def game():
    global h_x, h_y, e_x, e_y, e2_x, e2_y, torpeda_x, torpeda_y, torpeda_xs, torpeda_ys, torpeda_flag, e_boom, e2_boom, e_boom_time, e2_boom_time, boom_max_time, h_score, h_score_next_level, h_hp, state, h_level, bg
    #Действия
    if b_left == True:
        h_x -= h_xs
        if h_x + h_img.get_width()  <=0:
            h_x = 800
    if b_right == True:
        h_x += h_xs
        if h_x  >= 800:
            h_x = 0 - h_img.get_width()         

    ######### Рисование
    # Рисуем фон
    screen.blit(bg,[0,0])

    draw_bg_anim()

    # Рисуем первого противника, если взрыв или нету взрыва
    if e_boom == True:
        e_boom_time -= 1
        if e_boom_time <=0:
            e_boom_time = boom_max_time
            e_boom = False
            e_x = 0 - rnd.randint(100,500)            
        for i in range(0,10):
            q = e_x + rnd.randint(0,e_img.get_width())
            w = e_y + rnd.randint(0,e_img.get_height())
            screen.blit(boom_img,[q,w])
    else:
        #Противник 1
        e_x += e_xs
        if e_x >= 800:
            e_x = 0 - e_img.get_width()
            e_boom = False
            h_hp -= 1   
        screen.blit(e_img,[e_x,e_y])
            
    if e2_boom == True:
        e2_boom_time -= 1
        if e2_boom_time <=0:
            e2_boom_time = boom_max_time
            e2_boom = False
            e2_x = 0 - rnd.randint(100,500)
        for i in range(0,10):
            q = e2_x + rnd.randint(0,e2_img.get_width())
            w = e2_y + rnd.randint(0,e2_img.get_height())
            screen.blit(boom_img,[q,w])
    else:
        #Противник 2
        e2_x -= e2_xs
        if e2_x <= 0 - e2_img.get_width():
            e2_x = 800
            h_hp -= 1
        screen.blit(e2_img,[e2_x,e2_y])

    # Если закончились очки здоровья, то переключаемся в gameover
    if h_hp <=0:
        state = 3
        
    #Выстрел
    if torpeda_flag == True:
        torpeda_y -= torpeda_ys
        if torpeda_y + torpeda_img.get_height() <=0:
            torpeda_flag = False

        torpeda_c = torpeda_x + torpeda_img.get_width() // 2
        #Первый противник
        xb = torpeda_c > e_x and torpeda_c < e_x + e_img.get_width()
        yb = torpeda_y < e_y + e_img.get_height()  and torpeda_y > e_y
        if xb and yb:
            channel = fire.stop()
            channel2 = fire2.play()
            e_boom = True
            torpeda_flag = False
            h_score += 100
        else:
            screen.blit(torpeda_img,[torpeda_x,torpeda_y])

        #Второй противник
        xb = torpeda_c > e2_x and torpeda_c < e2_x + e2_img.get_width()
        yb = torpeda_y < e2_y + e2_img.get_height()  and torpeda_y > e2_y
        if xb and yb:
            channel = fire.stop()
            channel2 = fire2.play()            
            e2_boom = True
            torpeda_flag = False
            h_score += 100
        else:
            screen.blit(torpeda_img,[torpeda_x,torpeda_y])            
    #Переход на следующий уровень
    if h_score >= h_score_next_level:
        h_level += 1
        print(h_level)
        h_score_next_level += 1000
        try:
            bg = pyg.image.load('fon%s.png'%(h_level)).convert_alpha()
        except:
            pass
    #Если все уровни пройдены, то победа
    if h_level >= 4:
        state = 2
        pyg.mixer.music.load('music2.mp3')
        pyg.mixer.music.play()
    # Рисуем нашего персонажа
    screen.blit(h_img,[h_x,h_y])

    draw_gui()

def draw_bg_anim():
    global frame_cur, frame, anim1_x, anim2_x,anim2_y, anim2_xs, anim2_ys, frame_cur3, frame3, anim3_x, anim3_x,anim3_y, anim3_xs, anim3_ys
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

    frame3 -= 1
    if frame3 <=0:
        frame_cur3 += 1
        # Вот тут какая-то ерунда
        if frame_cur3 > len(anim3)-1:
            frame_cur3 = 0
        #---------------------
        frame3 = frame_max3
    anim3_x += anim3_xs
    if anim3_x > 800:
        anim3_x = 0 - anim3[0].get_width()    
    screen.blit(anim3[frame_cur3],[anim3_x,anim3_y])    

def draw_gui():
    # Рисуем GUI
    #pyg.draw.rect(screen, (255,0,0),(0,600-30,800,600),0)
    t = "SCORE: %s      HP: %s      Level: %s"%(h_score,h_hp, h_level)
    text_color = (255,255,255)
    text = font1.render(t,True,text_color)
    x = 50
    y = 600 - text.get_height()
    # отрисовываем текст
    screen.blit(text,[x,y])    

def gameover():
    global bo1_x, frame_cur, frame, anim1_x, anim2_x,anim2_y, anim2_xs, anim2_ys, torpeda_x, torpeda_y, torpeda_xs, torpeda_ys
    screen.blit(bg,[0,0])

    t = "G A M E O V E R"
    text_color = (255,0,0)
    text = font.render(t,True,text_color)
    x = screen.get_width() // 2 - text.get_width() // 2
    y = screen.get_height() // 2 - text.get_height() // 2
    # отрисовываем текст
    screen.blit(text,[x,y])


def win():
    global bo1_x, frame_cur, frame, anim1_x, anim2_x,anim2_y, anim2_xs, anim2_ys, torpeda_x, torpeda_y, torpeda_xs, torpeda_ys
    screen.blit(bg,[0,0])

    t = "W I N"
    text_color = (255,0,0)
    text = font.render(t,True,text_color)
    x = screen.get_width() // 2 - text.get_width() // 2
    y = screen.get_height() // 2 - text.get_height() // 2
    # отрисовываем текст
    screen.blit(text,[x,y])

def pause():
    global bo1_x, frame_cur, frame, anim1_x, anim2_x,anim2_y, anim2_xs, anim2_ys, torpeda_x, torpeda_y, torpeda_xs, torpeda_ys
    screen.blit(bg,[0,0])

    t = "P A U S E"
    text_color = (255,0,0)
    text = font.render(t,True,text_color)
    x = screen.get_width() // 2 - text.get_width() // 2
    y = screen.get_height() // 2 - text.get_height() // 2
    # отрисовываем текст
    screen.blit(text,[x,y])

while isGame:
    #События
    for e in pyg.event.get():
        if e.type == QUIT:
                isGame = False
        if e.type == KEYDOWN:
            if state == 0:
                state = 1
            if state == 3:
                isGame = False
            if e.key == K_ESCAPE:
                isGame = False
            if e.key == K_LEFT:
                b_left = True
                b_right = False
            if e.key == K_RIGHT:
                b_right = True
                b_left = False
            if e.key == K_p:
                if state == 4:
                    state = 1
                else:
                    state = 4
                    
            if e.key == K_SPACE:
                if torpeda_flag == False:
                    channel2 = fire2.stop()
                    channel = fire.play()
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
        pause()
        
    #Отображение
    pyg.display.flip()
    #Пауза
    clock.tick(60)
pyg.quit()
quit()
