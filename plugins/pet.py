from CybrocksLibrary import *
import base64
import random as R

petI = None
petI2 = None
xres = None
yres = None
bgcolor = None
borderC = None
data = []

def init(settingsdata):
    global petI,xres,yres,petI2

    #load image of slime
    image = base64.b64decode(b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAkklEQVQ4je2SKxKAMAxEl0xPEYfGIREcHlGJQ+N6CqbF8EloCsxgWUUL+7JLC/z6rKr4htqk1nE0v3UlI8dGbQdCskAaQG2SxtD1xzN7ARIQKpmv2mEcG1WPig4A7AcTokLL6bXxS0ywSJElqOEU6CnFbYU3Oo/EqDFjySazHxBoOo4zKy1NUtcqeYItxavc4h6s1Gs0zvcqAy0AAAAASUVORK5CYII=')

    xres = settingsdata['RESx']
    yres = settingsdata['RESy']
    petI = BetterImage(image, (0, yres-16), 1, 1)
    petI2 = BetterImage(image, (55, yres-64-85),4, 4)
    
    
def update(idedata):
    global bgcolor, borderC, data
    data = idedata
    #move sime like the little scroll tingy on the side but on the bottom
    petI.move((((idedata[0]+0.0001) / (idedata[2]+0.0001)) * xres, yres - 16)) #the +0.0001 is to prevent DB0 error
    bgcolor = idedata[6][4]
    borderC = idedata[6][5]
    

def draw(window):
    if petI is not None: #this prevents an error
        petI.draw(window)

def drawpanel(window):
        if data:
            pg.draw.rect(window, bgcolor, [40, data[7]['RESy']-64-95, 100, 100])
            pg.draw.rect(window, borderC, [40, data[7]['RESy']-64-95, 100, 100],5)
            petI2.draw(window)

def drawoverlay(window):
    pass