
#this is a code editor for the engine and I would eventually like to make it into my main


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


def main(script=[],SfilePath='',projfolder=''):
    
    # -------== setting up ==--------------------------------------------------------------------------------------------------------------
    
    #load the settings.json
    with open('settings.json', "r", encoding="utf-8") as f:
        data = json.load(f)

    #the usual stuff
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    clock = pg.time.Clock()
    
    window = pg.display.set_mode((data["RESx"],data["RESy"]), pg.NOFRAME)
    sdl_window = Window.from_display_module()
    
    font = pg.font.Font('IDEresources/fonts/MapleMono-NF-Regular.ttf', 15)
    sideFont = pg.font.Font('IDEresources/fonts/MapleMono-NF-Bold.ttf', 15)
    
    code = script
    line = ''
    name = ''

    projfolder = projfolder

    version = 'B1.0:8/11/2026'

    '''loaded_lines = load().splitlines()

    if loaded_lines:
        code = loaded_lines[:-1]
        line = loaded_lines[-1]'''
    

    lookingatline = 1#len(code) + 1
    uppercase = False
    scrolly = 0

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

    ftype = Path(SfilePath).suffix.lstrip(".")

    #right now its manual for this script \/ \/
    if ftype == 'cobra': #load programing languages ----------------------------------------------------------------
        specialwords = load_language("cobra.json", pallet, p)
    elif ftype == 'py':
        specialwords = load_language("python.json", pallet, p)
    elif ftype == 'jspn':
        specialwords = load_language("json.json", pallet, p)
    else:
        specialwords = load_language("python.json", pallet, p)

    
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
                elif pg.key.name(event.key) == "f2":
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
                    root = tk.Tk()
                    root.withdraw()

                    projfolder = filedialog.askdirectory(title="Select Project Folder")

                    root.destroy()

                    if projfolder:
                        print("Project folder:", projfolder)

                    #print(projfolder)

                elif pg.key.name(event.key) == "f4":

                    if projfolder:
                        save(code + [line], name, SfilePath)

                        filename = os.path.basename(SfilePath)

                        subprocess.run(
                            [sys.executable, filename],
                            cwd=projfolder
                        )
                    else:
                        print("No project folder selected. Press F3 first.")

                elif pg.key.name(event.key) == "f5":
                    specialwords = load_language(data["lang1"], pallet, p)

                elif pg.key.name(event.key) == "f6":
                    specialwords = load_language(data["lang2"], pallet, p)

                elif pg.key.name(event.key) == "f7":
                    specialwords = load_language(data["lang3"], pallet, p)
                            
                elif pg.key.name(event.key) == "f8":
                    specialwords = load_language(data["lang4"], pallet, p)
                elif pg.key.name(event.key) == "f9":
                    pass
                elif pg.key.name(event.key) == "f10":
                    pass
                elif pg.key.name(event.key) == "f11":
                    pass
                elif pg.key.name(event.key) == "f12":
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
                elif pg.key.name(event.key) == "escape": #quit
                    #running = False
                    pass
                elif pg.key.name(event.key) == "return": #enter
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
        if keys[pg.K_PAGEDOWN]:
            if keys[pg.K_LSHIFT]:
                lookingatline += 2
                scrolly += 2
            else:
                lookingatline += 1
                scrolly += 1
        if keys[pg.K_PAGEUP]:
            if keys[pg.K_LSHIFT]:
                if lookingatline >=1:
                    lookingatline -= 2
                else:
                    lookingatline = 1
                if scrolly >= 2:
                    scrolly -= 2
                else:
                    scrolly=0
            else:
                if lookingatline !=1:
                    lookingatline -= 1
                if scrolly != 0:
                    scrolly -= 1

        # -------== buttons ==--------------------------------------------------------------------------------------------------------------
        if closeB.is_pressed():
            running = False

        if minB.is_pressed():
            pg.display.iconify()




        # -------== drawing ==--------------------------------------------------------------------------------------------------------------
        window.fill(bg)
        pg.draw.rect(window, margin, [0, 30, 45, 2000])
        
        current_y = 35 + ((lookingatline - 1) * 25) - (scrolly * 25)
        pg.draw.rect(window,textHighlight,(45, current_y, 2000, 25))
              

        y = 35

        for i in range(M.floor((data["RESy"]-90)/25)):
            numbers = sideFont.render(str(1 + i + scrolly),False,text1)
            window.blit(numbers, (5, i * 25 + 40))

            code_index = i + scrolly

            if code_index < len(code):
                drawcolorwords(window,font,code[code_index],50,y)

            y += 25


        
            
        line2 = str(line) + '<|' #cursor -------------------------------------------------------
        drawcolorwords(window, font, line2, 50, (lookingatline*25+12)-(scrolly*25))
        
        pg.draw.rect(window, titleBar, [0, 0, 2000, 30])
        pg.draw.rect(window, main, [0, data["RESy"]-60, 2000, 60])

        drawcolorwords(window, font, str(lookingatline), 10, data["RESy"]-40)
        drawcolorwords(window, font, line2, 50, data["RESy"]-40)

        title = font.render(f'Cy IDE {version}                      {name}',False,(255,255,255))
        window.blit(title,(5,5))
        
        closeB.draw(window)  
        minB.draw(window)


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


if __name__ == "__main__":
    
    main()


def Sload(path):
    
    with open(path, "r") as f:
        return f.read().splitlines()


def run(script):
    S = Sload(script)
    SfilePath = script
    main(S,SfilePath)


pg.quit()