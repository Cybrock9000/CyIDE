
#This is an example of a ui type plugin for the panel

from CybrocksLibrary import *
import base64
import random as R
import psutil

fpsT = None
xres = None
yres = None
bgcolor = None
borderC = None
ramPT = None
ramGT = None
cpuT = None
title = None

ram = psutil.virtual_memory()

def init(settingsdata):
    global xres,yres, bgcolor, borderC

    xres = settingsdata['RESx']
    yres = settingsdata['RESy']


def update(idedata):
    global fpsT,ramPT,ramGT,cpuT,title, bgcolor, borderC
    title = idedata[5].render(f'CyIDE Extras Plugin V1',False,idedata[6][1])
    fpsT = idedata[5].render(f'FPS: {idedata[4]}',False,idedata[6][1])
    ramPT = idedata[5].render(f'Total Ram used%: {ram.percent}',False,idedata[6][1])
    ramGT = idedata[5].render(f'Total Ram used GB: {round(ram.used / 1e9, 2)}',False,idedata[6][1])
    cpuT = idedata[5].render(f'Total CPU used%: {round(psutil.cpu_percent())}',False,idedata[6][1])
    bgcolor = idedata[6][4]
    borderC = idedata[6][5]



def draw(window):
    pass

def drawpanel(window):
    if fpsT and bgcolor and borderC: #this prevents an error
        pg.draw.rect(window, bgcolor, [40, 30, 250, 100])
        pg.draw.rect(window, borderC, [40, 30, 250, 100],5)
        window.blit(title,(50,40))
        window.blit(fpsT,(50,55))
        window.blit(ramPT,(50,70))
        window.blit(ramGT,(50,85))
        window.blit(cpuT,(50,100))

def drawoverlay(window):
    pass