# 2026 Cy

import pygame as pg
from pygame.locals import *
from pygame._sdl2 import Window
import os
import tkinter as tk
from tkinter import filedialog
import sys
from CybrocksLibrary import *
import json
from pathlib import Path
import subprocess
import math as M
from plugin_manager import pluginM


def main(script=[],SfilePath='',projfolder=''):
    
    # -------== setting up ==--------------------------------------------------------------------------------------------------------------
    
    #load the settings.json
    with open('settings.json', "r", encoding="utf-8") as f:
        data = json.load(f)

    #the usual stuff
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    clock = pg.time.Clock()
    window = pg.display.set_mode((0,0),pg.FULLSCREEN, pg.NOFRAME)
    #window = pg.display.set_mode((data["RESx"],data["RESy"]), pg.NOFRAME)
    sdl_window = Window.from_display_module()
    
    font = pg.font.Font('IDEresources/fonts/MapleMono-NF-Regular.ttf', 15)
    sideFont = pg.font.Font('IDEresources/fonts/MapleMono-NF-Bold.ttf', 15)
    
    code = script
    line = ''
    name = ''

    projfolder = projfolder
    filename = os.path.basename(SfilePath)

    version = 'B1.0:8/12/2026'

    '''loaded_lines = load().splitlines()

    if loaded_lines:
        code = loaded_lines[:-1]
        line = loaded_lines[-1]'''
    

    lookingatline = 1#len(code) + 1
    uppercase = False
    scrolly = 0
    scrollx = 0
    tab = False #opens that side menu, called it tab because its like a tab
    shifting = False



    pluginManager = pluginM()
    pluginManager.init(data)

    # -------== colors ==--------------------------------------------------------------------------------------------------------------

    pallet = pg.image.load((os.getcwd() + "/IDEresources/textures/p.png")) #thanks to the people on stack overflow for loading colors from a pic
    image_rect = pallet.get_rect()
    
    window.fill((0,0,0))
    window.blit(pallet, image_rect)
    screensurf = pg.display.get_surface() #gets colors from picture for more customization
    
    p = data["pallet"] #pallet, which is y so there could be multiple in one pic

    main = screensurf.get_at((0,p))
    bg = screensurf.get_at((1,p))
    margin = screensurf.get_at((3,p))
    textHighlight = screensurf.get_at((4,p))
    text1 = screensurf.get_at((2,p))
    titleBar = screensurf.get_at((5,p))
    tab1 = screensurf.get_at((15,p))
    tab2 = screensurf.get_at((14,p))
    tab3 = screensurf.get_at((7,p))

    ftype = Path(SfilePath).suffix.lstrip(".")

    #right now its manual for this script \/ \/
    if ftype == 'cobra': #load programing languages ----------------------------------------------------------------
        specialwords = load_language("cobra.json", pallet, p)
    elif ftype == 'py':
        specialwords = load_language("python.json", pallet, p)
    elif ftype == 'jspn':
        specialwords = load_language("json.json", pallet, p)
    else:
        specialwords = load_language("text.json", pallet, p)
        

    
    def drawcolorwords(surface, font, text, x, y):
        words = text.split(" ")

        cx = x

        for word in words: #checks to see if its in the list and colors it here
            color = text1 #normal text

            for keyword, data in specialwords.items(): 
                kcolor = data[0]
                mode = data[1]

                if mode == 0:
                    if word == keyword: #color only if its exact like as
                        color = kcolor
                        break

                elif mode == 1:
                    if word.startswith(keyword): #color the full thing like print() (or even printasdjfhlaksjdhf wich i will have to fix soon)
                        color = kcolor
                        break

            rendered = font.render(word, True, color)
            surface.blit(rendered, (cx, y))

            cx += rendered.get_width()

            space = font.render(" ", True, text1)
            surface.blit(space, (cx, y))
            cx += space.get_width()

    closeB = Button(os.getcwd() +"/IDEresources/textures/closeB.png", (data["RESx"]-25,5), 1, 1)
    minB = Button(os.getcwd() +"/IDEresources/textures/minB.png", (data["RESx"]-55,5), 1, 1)


    running = True
    while running:


        # -------== key buttons ==--------------------------------------------------------------------------------------------------------------
        for event in pg.event.get():
            
            if event.type == MOUSEWHEEL:
                        scrolly -= event.y
            if scrolly <= 0:
                        scrolly = 0
                        
            if event.type == pg.KEYDOWN:

                if pg.key.name(event.key) == "space":
                    line = line + ' '
                elif pg.key.name(event.key) == "tab":
                    line = line + '    '
                elif pg.key.name(event.key) == "backspace":
                    if line == '':
                        if lookingatline != 1:
                            lookingatline -= 1
                            line = code.pop(lookingatline -1)
                    else:
                        line = line[:-1]
                elif pg.key.name(event.key) == "left shift": #all these blank passes to prevent you doing = hleft shiftello
                    pass
                elif pg.key.name(event.key) == "right shift":
                    pass
                elif pg.key.name(event.key) == "left ctrl":
                    pass
                elif pg.key.name(event.key) == "right ctrl":
                    pass
                elif pg.key.name(event.key) == "left alt":
                    pass
                elif pg.key.name(event.key) == "right alt":
                    pass
                elif pg.key.name(event.key) == "caps lock":
                    if uppercase == True:
                        uppercase = False
                    else:
                        uppercase = True
                elif pg.key.name(event.key) == "f1": #(maybe) temporary save
                    save(code + [line],name,SfilePath)
                elif pg.key.name(event.key) == "f2": #load file and folder its in
                    loaded, specialwords, name = load(pallet,p,specialwords)

                    if loaded:
                        lines = loaded.splitlines()

                        if lines:
                            code = lines[:-1]
                            line = lines[-1]
                        else:
                            code = []
                            line = ""

                        lookingatline = len(code) + 1
                        code.insert(lookingatline-1,line)
                        line = ""
                        lookingatline = 1
                        projfolder = os.path.dirname(name)
                        SfilePath = os.path.basename(name)
                        
                elif pg.key.name(event.key) == "f3":
                    pass
                elif pg.key.name(event.key) == "f4": #run it
                    save(code + [line], name, SfilePath)

                    filename = os.path.basename(SfilePath)

                    subprocess.run([sys.executable, filename],cwd=projfolder)

                elif pg.key.name(event.key) == "f5":
                    #specialwords = load_language(data["lang1"], pallet, p)
                    pass

                elif pg.key.name(event.key) == "f6":
                    #specialwords = load_language(data["lang2"], pallet, p)
                    pass

                elif pg.key.name(event.key) == "f7":
                    #specialwords = load_language(data["lang3"], pallet, p)
                    pass
                            
                elif pg.key.name(event.key) == "f8":
                    #specialwords = load_language(data["lang4"], pallet, p)
                    pass
                
                elif pg.key.name(event.key) == "f9":
                    pass
                elif pg.key.name(event.key) == "f10":
                    pass
                elif pg.key.name(event.key) == "f11":
                    pass
                elif pg.key.name(event.key) == "f12":
                    pass
                elif pg.key.name(event.key) == "PAGE UP":
                    pass
                elif pg.key.name(event.key) == "PAGE DOWN":
                    pass
                elif event.key == pg.K_UP:
                    if lookingatline != 1:
                        lookingatline -= 1

                elif event.key == pg.K_DOWN:
                    lookingatline += 1
                    if len(code) <= (lookingatline - 1):
                        code.insert(lookingatline-1,line)
                        line = ""

                elif pg.key.name(event.key) == "numlock":
                    pass
                elif pg.key.name(event.key) == "escape": # was quit
                    save(code + [line],name,SfilePath)
                    settings(window,p,font,script=[],SfilePath='',projfolder='')
                    running = False
                    #pass
                elif pg.key.name(event.key) == "return": #enter
                    if shifting:
                        code.insert(lookingatline-1,line)
                        lookingatline += 1
                    else:
                        code.insert(lookingatline-1,line)
                        line = ""
                        lookingatline += 1
                else:
                    if uppercase:
                        line += pg.key.name(event.key).upper()
                    else:
                        line += event.unicode
                
                #print(lookingatline)
                #print(pg.key.name(event.key))


        keys = pg.key.get_pressed()
        #print(keys)
        if keys[pg.K_F3]:
            tab = True
        else:
            tab = False

        if keys[pg.K_LSHIFT]:
            shifting = True
        else:
            shifting = False

        if keys[pg.K_LCTRL]:
            control = True
        else:
            control = False

        if keys[pg.K_PAGEDOWN]:
            if shifting:
                lookingatline += 2
                scrolly += 2
            elif control:
                if scrollx <= -10:
                    scrollx += 10
            else:
                lookingatline += 1
                scrolly += 1

        if keys[pg.K_PAGEUP]:
            if shifting:
                if lookingatline >=1:
                    lookingatline -= 2
                else:
                    lookingatline = 1
                if scrolly >= 2:
                    scrolly -= 2
                else:
                    scrolly=0
            elif control:
                scrollx -= 10
            else:
                if lookingatline !=1:
                    lookingatline -= 1
                if scrolly != 0:
                    scrolly -= 1

            if lookingatline <=0:
                lookingatline = 1

        pluginManager.update(idedata=(scrolly,scrollx,len(code),keys,clock.get_fps(),font,(tab,tab1,tab2,tab3,margin,text1),data))

        #print(scrollx)


        
        # -------== buttons ==--------------------------------------------------------------------------------------------------------------
        if closeB.is_pressed():
            running = False

        if minB.is_pressed():
            pg.display.iconify()





        # -------== drawing ==--------------------------------------------------------------------------------------------------------------
        window.fill(bg)
        
        current_y = 35 + ((lookingatline - 1) * 25) - (scrolly * 25)
        pg.draw.rect(window,textHighlight,(45, current_y, 2000, 25))

        y = 35   
        for i in range(M.floor((data["RESy"]-90)/25)):
            code_index = i + scrolly
        
            if code_index < len(code):
                drawcolorwords(window,font,code[code_index],50+scrollx,y)
        
            y += 25

        pg.draw.rect(window, margin, [0, 30, 45, 2000])

        for i in range(M.floor((data["RESy"]-90)/25)):
            numbers = sideFont.render(str(1 + i + scrolly),False,text1)
            window.blit(numbers, (5, i * 25 + 40))

            
        line2 = str(line) + '<|' #cursor -------------------------------------------------------
        drawcolorwords(window, font, line2, 50, (lookingatline*25+12)-(scrolly*25))
        
        pg.draw.rect(window, titleBar, [0, 0, 2000, 30])
        pg.draw.rect(window, main, [0, data["RESy"]-60, 2000, 60])

        drawcolorwords(window, font, str(lookingatline), 10, data["RESy"]-40)
        drawcolorwords(window, font, line2, 50, data["RESy"]-40)

        pluginManager.draw(window)

        if tab:
            filename = os.path.basename(SfilePath)
            pg.draw.rect(window, margin, [data['RESx']-(data['RESx']/4), 30, data['RESx']/4, data['RESy']-90])
            pg.draw.rect(window, text1, [data['RESx']-(data['RESx']/4), 30, data['RESx']/4, data['RESy']-90],5)
            pg.draw.rect(window, text1, [data['RESx']-(data['RESx']/4), data['RESy']/4, data['RESx']/4, 5])
            ploaded = font.render(f'Plugins loaded: {len(pluginManager.pluginsloaded)}',False,tab1)
            window.blit(ploaded,((data['RESx']-(data['RESx']/4))+10,40))

            sy = 70
            if pluginManager.pluginsloaded:
                for plugin in pluginManager.pluginsloaded:
                        pluginT = font.render(f'{plugin}',False,tab2)
                        window.blit(pluginT,((data['RESx']-(data['RESx']/4))+10,sy))
                        sy += 20
            else:
                pluginT = font.render(f'None',False,tab2)
                window.blit(pluginT,((data['RESx']-(data['RESx']/4))+10,sy))
                sy += 20

            ftype = Path(SfilePath).suffix.lstrip(".")

            filenameT = font.render(f'Filename: {filename}',False,tab1)
            window.blit(filenameT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+10))

            if ftype == 'py':
                filetypeT = font.render(f'Filetype: Python',False,tab1)
                window.blit(filetypeT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+30))
            elif ftype == 'cobra':
                filetypeT = font.render(f'Filetype: Cobra',False,tab1)
                window.blit(filetypeT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+30))
            elif ftype == 'txt':
                filetypeT = font.render(f'Filetype: Text',False,tab1)
                window.blit(filetypeT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+30))
            else:
                filetypeT = font.render(f'Filetype: {ftype}',False,tab1)
                window.blit(filetypeT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+30))

            linesT = font.render(f'Lines: {len(code)}',False,tab1)
            window.blit(linesT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+50))
            filesTT = font.render(f'Files in dir:',False,tab1)
            window.blit(filesTT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+70))

            sy = 90
            if projfolder:
                for file in os.listdir(projfolder):
                    if file == filename:
                        filesT = font.render(f'{file}',False,tab3)
                        window.blit(filesT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+sy))
                        sy += 20
                    else:
                        filesT = font.render(f'{file}',False,tab2)
                        window.blit(filesT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+sy))
                        sy += 20
            else:
                filesT = font.render(f'None',False,tab2)
                window.blit(filesT,((data['RESx']-(data['RESx']/4))+10,(data['RESy']/4)+sy))


            pluginManager.drawpanel(window)


        title = font.render(f'Cy IDE {version}                      {name}',False,(255,255,255))
        window.blit(title,(5,5))
        
        closeB.draw(window)  
        minB.draw(window)

        pluginManager.drawoverlay(window)

        clock.tick(30)
        pg.display.flip()
        



def save(code,name,SfilePath=''):
    if name == '':
        root = tk.Tk()
        root.title("Name and file type. (example = file.txt)")


        tk.Label(root, text="Name and file type. (example = file.txt)").grid(row=0, column=0)

        nameEntry = tk.Entry(root)
        nameEntry.grid(row=1, column=0)

        def submit():
            nonlocal name
            name = nameEntry.get()
            root.destroy()

        submitButton = tk.Button(root, text="OK", command=submit)
        submitButton.grid(row=2, column=0, columnspan=2)

        root.mainloop()
    if name != '':
        with open(name, "w") as f:
            for line in code:
                f.write(line + "\n")
    return name


def load(pallet,p,specialwords):
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename(title="Open File",filetypes=[("All Files", "*.*")])

    root.destroy()

    if not filename:
        return None, specialwords

    ftype = Path(filename).suffix.lower().lstrip(".")
    if ftype == 'cobra':
            specialwords = load_language("cobra.json", pallet, p)
    elif ftype == 'py':
            specialwords = load_language("python.json", pallet, p)
    elif ftype == 'jspn':
            specialwords = load_language("json.json", pallet, p)
    else:
            specialwords = load_language("python.json", pallet, p)

    with open(filename, "r") as f:
        return f.read(), specialwords, filename


def load_language(filename, screensurf, p):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"IDEresources","languages",filename)

        with open(path, "r", encoding="utf-8") as f:
            specialwords = json.load(f)

        for keyword, data in specialwords.items():
            palette_index = data[0]
            data[0] = screensurf.get_at((palette_index, p))

        print("Loaded language:", filename)
        

        return specialwords


def Sload(path):
    
    with open(path, "r") as f:
        return f.read().splitlines()


def run(script):
    S = Sload(script)
    SfilePath = script
    main(S,SfilePath)



def settings(window,p,font,script=[],SfilePath='',projfolder=''):

    with open('settings.json') as f:
        data = json.load(f)

    title = font.render(f'CyIDE Settings',False,(255,255,255))

    updelay = False
    downdelay = False

    clock = pg.time.Clock()

    pallet = BetterImage((os.getcwd() + "/IDEresources/textures/p.png"),(data['RESx']/2,20),20,20)
    pointer = BetterImage((os.getcwd() + "/IDEresources/textures/pointer.png"),(data['RESx']/2-32,p*20+20),1,1)

    up = Button((os.getcwd() + "/IDEresources/textures/up.png"),(data['RESx']/2-64,20),2,2)
    down = Button((os.getcwd() + "/IDEresources/textures/down.png"),(data['RESx']/2-64,45),2,2)
    '''up = Button((os.getcwd() + "/IDEresources/textures/up.png"),(data['RESx']/2-64,20),2,2)
    down = Button((os.getcwd() + "/IDEresources/textures/down.png"),(data['RESx']/2-64,45),2,2)'''

    sts = Button((os.getcwd() + "/IDEresources/textures/sts.png"),(0,80),2,2)

    running = True
    while running:


        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == "escape": # quit
                    subprocess.Popen([sys.executable, "CYeditor.py"]) # <<<<<<<<<<<< CHANGE THIS TO EXE WHEN COMPILED <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    running = False


        if up.is_pressed() and updelay == False:
            data['pallet'] = data['pallet'] - 1
            p -= 1

            with open('settings.json', "w") as f:
                json.dump(data, f)
            updelay = True
                    
        elif up.is_pressed() and updelay == True:
            pass
        else: 
            updelay = False


        if down.is_pressed() and downdelay == False:
            data['pallet'] = data['pallet'] + 1
            p += 1
            with open('settings.json', "w") as f:
                json.dump(data, f)
            downdelay = True
                            
        elif down.is_pressed() and downdelay == True:
            pass
        else: 
            downdelay = False

        xrest = font.render(f'X Resolution: {data['RESx']}',False,(255,255,255))
        yrest = font.render(f'Y Resolution: {data['RESy']}',False,(255,255,255))


        window.fill((0,0,0))
        window.blit(title,(0,0))
        window.blit(xrest,(0,100))
        window.blit(yrest,(0,120))
        pallet.draw(window)

        pointer.move((data['RESx']/2-32,p*20+20))
        pointer.draw(window)

        up.draw(window)
        down.draw(window)
        #sts.draw(window)

        clock.tick(30)
        pg.display.flip()





if __name__ == "__main__":
    
    main()



pg.quit()
sys.exit()