# Cactus Whid HTTP keystrokes POC
# --------------------------------------------------------------
# by B3RT1NG
# https://github.com/b3rt1ng
# --------------------------------------------------------------
# Feel like your WHID is BORRING ???
# Fear not, i've got the solution for you my dear.
# Beware, the OMEGA WHIDE LIVE KEYBOARD
# 
# I just thought having a live keyboard on another machine would be sick
# and i got a cactus whid at hand so why not ? 

import pygame, requests, subprocess
from threading import Thread
from time import time,sleep
from random import randint

from sqlalchemy import true
from kbmap import map

# settings variables, modify them as you need
timeout = 2 # set the TO before sending the sentence
# because i felt like sending a request per character felt a little to heavy, i decided to let you build your sentence then send it once you finished typing
autosend = True # will send automatically the sentence
rage = 10

pygame.init()
pygame.mixer.init()

ping = "host unreachable"
host = "192.168.1.1"
red = (10,0,0)
grey = (44, 47, 51)
white = (255, 255, 255)
fire = (255,50,0)
black = (35, 39, 42)
light_grey = (153, 170, 181)
blue = (114, 137, 218)
X = 800
Y = 800
sentence = ""
history = []
sent = True
start = time()
wifi = pygame.transform.scale(pygame.image.load('wifi.png'), (X/10, Y/10))
head = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Connection': 'keep-alive',
  'Referer': 'http://192.168.1.1/inputmode',
  'Upgrade-Insecure-Requests': '1',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache'
}
stop = False

def ping_routine():
    """
    will ping the whid host every 2 seconds so we can display it
    """
    global ping, stop
    while True:
        if stop == True:
            return 0
        try:
            result = subprocess.run(
                ['ping', '-c', '1', host],
                text=True,
                capture_output=True,
                check=True)
            for line in result.stdout.splitlines():
                if "icmp_seq" in line:
                    ping = line.split('time=')[-1].split(' ms')[0]+' ms'
        except:
            ping = "host unreachable"
        sleep(2)


p = Thread(target=ping_routine)
p.start()

guns = [pygame.mixer.Sound("sfx/1.wav"),pygame.mixer.Sound("sfx/2.wav"),pygame.mixer.Sound("sfx/3.wav"),pygame.mixer.Sound("sfx/4.wav"),pygame.mixer.Sound("sfx/5.wav"),pygame.mixer.Sound("sfx/6.wav"),pygame.mixer.Sound("sfx/7.wav")]
fart = pygame.mixer.Sound("sfx/fart.wav")
gun = pygame.mixer.Sound("sfx/1.wav")
surface = pygame.display.set_mode((X, Y))

pygame.display.set_caption('omega WHID live keyboard V0.1')

font = pygame.font.Font('freesansbold.ttf', 32)

pygame.display.flip()

def fromto(color1,color2,percent):
    """
    make you got from color1 to color2 at a specific rate (0.1 = close to color1, 0.9 = close to color2)
    """
    if percent>1:
        return color2
    else:
        return (color1[0]-((color1[0]-color2[0])*percent),color1[1]-((color1[1]-color2[1])*percent),color1[2]-((color1[2]-color2[2])*percent))

def shaking(rectangle, intensity):
    """
    return a different rectangle position (0.1, close to the original, 0.9 far from the original one)
    note: the "rage" variable sets the maximum pixels difference
    """
    movex = randint(-rage,rage)*intensity if intensity<1 else randint(-rage,rage)*1
    movey = randint(-rage,rage)*intensity if intensity<1 else randint(-rage,rage)*1
    return (rectangle[0]+movex, rectangle[1]+movey, rectangle[2]+movex, rectangle[3]+movey)

while True:
    text = font.render(sentence, True, black, white)
    textRect = (0 if text.get_rect()[2]<X else 0-(text.get_rect()[2]-800),767,text.get_rect()[2] if text.get_rect()[2]>X else 800,34)
    surface.fill(grey)

    if (time()-start > 0.3):
        percent = (time()-start)/timeout if (time()-start)/timeout<100 else 100
    else:
        percent = 0

    pygame.draw.rect(surface, light_grey, pygame.Rect(0, 0, Y, Y/10))
    surface.blit(font.render(ping, True, white, light_grey), (100,25,80,80))
    surface.blit(wifi, (10, 0))

    for i in range(len(history)):
        surface.blit(font.render(history[i], True, white, grey), (10,80+33*i,800,800)) #history

    surface.blit(font.render(sentence, True, fromto(white,fire,percent), grey), shaking(textRect, percent) if sent==False else (0,0,0,0)) #typing render

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            guns[randint(0,len(guns)-1)].play()
            if event.key == 8:
                sentence = sentence[:-1]
            else:
                sentence = sentence + str(map[event.key])
                sent = False
            start = time()
        elif event.type == pygame.QUIT:
            pygame.quit()
            stop = True
            quit()
            exit()

    if (time() - start > timeout and autosend and not sent):
        fart.play()
        sent = True
        history.append(sentence)
        if ping != "host unreachable":
            print("sending "+sentence)
            requests.post('http://192.168.1.1/runlivepayload', headers = head, data = 'livepayloadpresent=1&livepayload=Print%3A'+sentence.replace(' ', '+'))
        else: 
            print("no host")
        sentence = ""

    pygame.display.update()
