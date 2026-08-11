import pygame as pg
from pygame import gfxdraw
from settings import *
from player import *
import time
import math as M
from map import*
from os import listdir
from CybrocksLibraryG import *
import os
from npc_handler import *
from npc import *
from light import *
from state import *


def main():
    # inits

    pg.init()
    pg.mixer.init()
    
    NpcHandler = npcHandler()
    
    with open(os.curdir +'/scripts/player.cy', "r") as f:
        playerS = f.read().splitlines()
        
    with open(os.curdir +'/objects/npc.cy', "r") as f:
        npcS = f.read().splitlines()

    window = pg.display.set_mode(RES)

    pg.mouse.set_visible(False)
    pg.event.set_grab(True)

    icon = pg.image.load(os.curdir +'\icon.ico').convert_alpha()
    pg.display.set_icon(icon)
    
    clock = pg.time.Clock()
    
    bgm = pg.mixer.Sound(os.curdir +'/resources/music/bg.wav')
    channel = bgm.play(-1)

    sky = BetterImage(os.curdir +"/resources/textures/sky.webp", (0, 0), 2, 2)
    sky2 = BetterImage(os.curdir +"/resources/textures/sky.webp", (0, 0), 2, 2)
    hand = BetterImage(os.curdir +"/resources/textures/w/handEmpty.png", (RES[0]/4+15, RES[1]/4), 5, 5)
    if EHUD == True:
        hud = BetterImage(os.curdir +"/resources/textures/hud.png", (0, 0), 2, 2)
    if DARK == 1:
        vig = BetterImage(os.curdir +"/resources/textures/Vignette.png", (0, 0), 2, 2)
    healthBar = BetterImage(os.curdir +"/resources/textures/health/healthFull.png", (200, 625), 8, 8)

    playerStartPos = (0, 0, 20)
    px,py,pz= playerStartPos
    
    
    jumping = False
    i = -20
    g = 0
    col = False
    grounded = True
    handbob = 0
    bobDir = 1
    pew = False
    
    SPEED, HEALTH, CanRun, CanCrouch = loadPlayerScripts(playerS)
    loadObjectScripts(npcS,NpcHandler)
    
    dx = 0
    dy = 0
    
    pa = 0
    pl = 0
    newwalldata = []


    running = True
    while running:
        
        dt = clock.tick(FPS) / 1000
        
        # controlls

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                running = False
                
        mx, my = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        rspeed = 200
        if keys[pg.K_LSHIFT] and not crouch and CanRun:
            crouch = False
            sprinting = True
            speed = SPEED * dt *2
        elif keys[pg.K_LCTRL] and not sprinting and CanCrouch:
            crouch = True
            sprinting = False
            speed = SPEED * dt /2
        elif not keys[pg.K_LCTRL]:
            crouch = False
            sprinting = False
            speed = SPEED * dt
            
        

        '''if keys[pg.K_LEFT]:
            pa -= rspeed * dt
            if pa < 0:
                pa +=360

        if keys[pg.K_RIGHT]:
            pa += rspeed * dt
            if pa > 359:
                pa -=360
        
        if keys[pg.K_UP]:
            pl += rspeed * dt

        if keys[pg.K_DOWN]:
            pl -= rspeed * dt'''
        
        if handbob >= 10:
            bobDir = -1
        if handbob <= -10:
            bobDir = 1

        if state.tool != "Empty":
            hand = BetterImage(os.curdir + f"/resources/textures/w/hand{state.tool}.png",(RES[0]/4+15, RES[1]/4),5, 5)
        else:
            hand = BetterImage(os.curdir + "/resources/textures/w/handEmpty.png",(RES[0]/4+15, RES[1]/4),5, 5)

            
        oldpx = px
        oldpy = py
        mx = 0
        my = 0

        if keys[pg.K_w]:
            mx += dx * speed
            my += dy * speed

        if keys[pg.K_s]:
            mx -= dx * speed
            my -= dy * speed

        if keys[pg.K_d]:
            mx += dy * speed
            my -= dx * speed

        if keys[pg.K_a]:
            mx -= dy * speed
            my += dx * speed

        px += mx
        for wall in wall_data: #kind of expencive
            if raycastCOL(window, px, py, pz, pa, wall[0], wall[1], wall[2], wall[3]):
                px = oldpx
                break
            
        py += my
        for wall in wall_data:
            if raycastCOL(window, px, py, pz, pa, wall[0], wall[1], wall[2], wall[3]):
                py = oldpy
                break
            
        mouse_buttons = pg.mouse.get_pressed()
        if mouse_buttons[0]:
            if pew == False:
                if state.tool == 'Gun':
                    pew = True
                    raycastShoot(window, px, py, pz, pa,NpcHandler)
        if not mouse_buttons[0]:
            pew = False

        #print(grounded)
        # jumping
        if keys[pg.K_SPACE] and grounded == True:
            grounded = False
            jumping = True
        
        if jumping == True:
            i += 1
            if not i >= 10: #jump height
                pz = (pz + (i/15)) # the number in (i/15) is speed
            else:
                jumping = False
                i = -20
        
            
        if pz <= 20 and jumping == False and crouch == False:
            falling = True
            pz +=0.01*g
  
            g += 100 *dt #gravity
        elif pz >= 20: 
            falling  = False
            grounded = True
            g = 0
        
        if crouch and grounded and not falling and not jumping:
            pz = 29
        elif not crouch and grounded and not falling and not jumping:
            pz = 20
        
            
        mdx, mdy = pg.mouse.get_rel() # mouse movement

        mdx = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, mdx))

        pa += (mdx * MOUSE_SENSITIVITY) *1.25 #looking r&r was too slow
 
        pl -= (mdy * MOUSE_SENSITIVITY_UD)/2 # you could snap your neck you were looking up too fast
        pl = max(-20, min(20, pl))
            
        if pa >= 360:
            pa -= 360
        if pa <= 0:
            pa += 360
            

        angle = pa * M.pi / 180
        
        #print(pl)

        dx = M.sin(angle)
        dy = M.cos(angle)

        #print(str(px) + ' ' + str(py) + ' ' + str(pz))

        # display
        
        pg.display.set_caption(f'{NAME}   FPS: {clock.get_fps():.1f}')
        window.fill('black')
        skyrot=5.2
        if -(pa*skyrot) >= 0:
            sky.move((-(pa*skyrot),-631+pl*30))
            sky2.move((-(pa*skyrot)-1875,-631+pl*30))
        else:
            sky.move((-(pa*skyrot),-631+pl*30))
            sky2.move((-(pa*skyrot)+1875,-631+pl*30))
        sky.draw(window)
        sky2.draw(window)
        
        angle = M.radians(pa)
        radcos = M.cos(angle) * 0.5
        radsin = M.sin(angle) * 0.5
        if FLOOR == 1:
            drawFloor(window, px, py, pz, pl, radcos, radsin)
        draw(window,px,py,pz,pa,pl,col,NpcHandler,radcos,radsin) #janky way on simple collision by using the draw method and raycaster, but it works for now
        NpcHandler.update((px,py),pa,pl,window,pz,wall_data)
            

        hand.draw(window)  
         
            
        if DARK == 1:
            vig.draw(window)

        if EHUD == True:
            hud.draw(window)     
            if HEALTH <=100:
                healthBar.new_image(os.curdir +"/resources/textures/health/healthFull.png", (200, 625), 8, 8)
            elif HEALTH <=80:
                healthBar.new_image(os.curdir +"/resources/textures/health/health80.png", (200, 625), 8, 8)
            elif HEALTH <=50:
                healthBar.new_image(os.curdir +"/resources/textures/health/health50.png", (200, 625), 8, 8)
            elif HEALTH <=25:
                healthBar.new_image(os.curdir +"/resources/textures/health/health25.png", (200, 625), 8, 8)
            elif HEALTH <=0:
                healthBar.new_image(os.curdir +"/resources/textures/health/health0.png", (200, 625), 8, 8)
            healthBar.draw(window)  
           

        pg.display.flip()
        
        

    pg.quit()
        

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def raycast(window, px, py, pz, pa, wx1, wy1, wx2, wy2):  # this checks if there is a wall the player can see
    #pg.draw.circle(window, "blue", (px, py), 5)

    for ray in range(rayAmount): #amount of rays
        
        #it is recomended to keep the fov (not the var, the cone) at around 90

        rayangle = (pa - 45 + ray * 3) * M.pi / 180 # the number *ing the ray is the angle between each ray

        dx = M.sin(rayangle)
        dy = M.cos(rayangle)

        

        rayend = (
            px + dx * rayDist,
            py + dy * rayDist
        )
        #pg.draw.line(window, "red", (px, py),rayend, 2)
        if intersect((px, py),rayend,(wx1, wy1), (wx2, wy2)):
                return False #a wall should be there


    return True #no wall :(


def raycastCOL(window, px, py, pz, pa, wx1, wy1, wx2, wy2):  # this checks for wall colision
    for ray in range(4): #amount of rays
        rayangle = (pa + ray * 90) * M.pi / 180 # the number *ing the ray is the angle between each ray

        dx = M.sin(rayangle)
        dy = M.cos(rayangle)

        sx, sy = px, py

        for move in range(15): #the dist the ray travels. AKA how fat you are
            sx += dx 
            sy += dy 
            #pg.draw.circle(window, "green", (sx, sy), 2)


            if intersect((px, py), (sx, sy),(wx1, wy1), (wx2, wy2)):
                return True #a wall is there

    return False #no wall

def raycastShoot(window, px, py, pz, pa, NpcHandler):
    rayangle = M.radians(pa)

    dx = M.sin(rayangle)
    dy = M.cos(rayangle)

    sx, sy = px, py

    for move in range(500):
        sx += dx
        sy += dy

        #pg.draw.circle(window, "blue", (int(sx), int(sy)), 2)

        for npc in NpcHandler.npc_list:
            if (intersect((px, py), (sx, sy),(npc.x - 10, npc.y - 10),(npc.x + 10, npc.y + 10)) or intersect((px, py), (sx, sy),(npc.x - 10, npc.y + 10),(npc.x + 10, npc.y - 10))):
                npc.remove = True
                return True

    return False
    

def reorderwalls(px, py): # for drawing order from furthest to closest
    wall_distances = []

    for wall in wall_data:
        x1, y1, x2, y2, c = wall

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        d = dist(px, py, mx, my)
        if d <= rayDist:
            wall_distances.append((d, wall))
            

    wall_distances.sort(reverse=True)

    return [wall for d, wall in wall_distances]

        
def npcraycast(handler, px, py, newwalldata):
    newwalldata = reorderwalls(px, py)

    for npc in handler.npc_list:
        npc.wall = True #set it first (totaly didnt have this effect me at first)

    for light in handler.light_list:
            light.wall = True
            
    for x1, y1, x2, y2, c in newwalldata:
        handler.raycast(px, py, x1, y1, x2, y2)
        handler.lraycast(px, py, x1, y1, x2, y2)





def drawFloor(window, px, py, pz, pl, radcos, radsin):

    near = 0.1
    draw = pg.draw.polygon

    for i in range(len(floorC)):
        screen_points = []

        #corners = [floorTL[i],floorTR[i],floorBR[i],floorBL[i]]
        tl = floorTL[i]
        tr = floorTR[i]
        br = floorBR[i]
        bl = floorBL[i]
        color = floorC[i]

        for wx, wy in (tl,tr,br,bl):

            x = wx - px
            y = wy - py

            rx = x * radcos - y * radsin
            rz = y * radcos + x * radsin

            if rz < near:
                rz = near

            rz_screen = 40-pz + ((pl * rz) / 32)

            inv = FOV / rz
            sx = rx * inv + 600
            sy = rz_screen * inv + 400

            screen_points.append((sx, sy))
            
        fx = (tl[0] + br [0]) / 2
        fy = (tl[1] + br [1]) / 2
        
        dx = fx - px
        dy = fy - py

        if dx*dx + dy*dy > rayDist*rayDist:
            continue
        
        if DARK == 1:
                    d = dist(px, py, fx, fy)
                    d = max(1, d)
                    c2 = (min(color[0], int(color[0] / d * SHADOW_DIST + 1)),min(color[1], int(color[1] / d * SHADOW_DIST + 1)),min(color[2], int(color[2] / d * SHADOW_DIST + 1)))
        else:
                    c2 = color
        draw(window, c2, screen_points)




def draw(window,px,py,pz,pa,pl,col,NpcHandler,radcos,radsin):    #drawing walls and such
    col = False
    newwalldata = reorderwalls(px, py)
    npcraycast(NpcHandler,px,py,newwalldata)
    draw = pg.draw.polygon
    
    for walls in range(len(newwalldata)):
        
        #radcos = M.cos(pa/180*M.pi)/2
        #radsin = M.sin(pa/180*M.pi)/2
        #radcos = M.cos(M.radians(pa))
        #radsin = M.sin(M.radians(pa))

        x1, y1, x2, y2, c = newwalldata[walls] # wall cords and color
        
        wx1, wy1 = x1 - px, y1 - py
        wx2, wy2 = x2 - px, y2 - py

        if raycast(window, px, py, pz, pa, x1, y1, x2, y2):
            continue
        
        #print(col)
        #pg.draw.line(window,c,(x1,y1),(x2,y2),2)
        
        socialdistfromcameradist = 0.1
        
        wallx[walls][0] = wx1 * radcos - wy1 * radsin
        wallx[walls][1] = wx2 * radcos - wy2 * radsin
        wallx[walls][2] = wallx[walls][0]
        wallx[walls][3] = wallx[walls][1]

        wally[walls][0] = wy1 * radcos + wx1 * radsin
        wally[walls][1] = wy2 * radcos + wx2 * radsin
        wally[walls][2] = wally[walls][0]
        wally[walls][3] = wally[walls][1]
        
        if dist(wallx[walls][1],wallx[walls][0],wallx[walls][3],wallx[walls][2]) <= 0:
            pass
        
        near = 0.1

        if wally[walls][0] < near:
            wally[walls][0] = near

        if wally[walls][1] < near:
            wally[walls][1] = near
            
        if wally[walls][2] < near:
            wally[walls][2] = near
        
        if wally[walls][3] < near:
            wally[walls][3] = near

        wallz[walls][0] = 0-pz+((pl*wally[walls][0])/32)
        wallz[walls][1] = 0-pz+((pl*wally[walls][1])/32)
        wallz[walls][2] = wallz[walls][0]+40
        wallz[walls][3] = wallz[walls][1]+40
        
        wallx[walls][0] = wallx[walls][0]*FOV/wally[walls][0]+600 #screen pos for x and y for both top and bottom of the wall
        wally[walls][0] = wallz[walls][0]*FOV/wally[walls][0]+400
        wallx[walls][1] = wallx[walls][1]*FOV/wally[walls][1]+600
        wally[walls][1] = wallz[walls][1]*FOV/wally[walls][1]+400
        wallx[walls][2] = wallx[walls][2]*FOV/wally[walls][2]+600
        wally[walls][2] = wallz[walls][2]*FOV/wally[walls][2]+400
        wallx[walls][3] = wallx[walls][3]*FOV/wally[walls][3]+600
        wally[walls][3] = wallz[walls][3]*FOV/wally[walls][3]+400
        
        
        '''if wallx[0]>0 and wallx[0]<1200 and wally[0]>0 and wally[0]<800:
            pg.draw.circle(window,'red',(wallx[0],wally[0]),3)
        if wallx[1]>0 and wallx[1]<1200 and wally[1]>0 and wally[1]<800:
            pg.draw.circle(window,'red',(wallx[1],wally[1]),3)'''
            
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        d = dist(px, py, mx, my)
        if d > rayDist:
            continue
        
        if DARK == 1:
            brightness = 0.0

            for light in NpcHandler.light_list:
                d = max(1.0, dist(mx, my, light.x, light.y))
                brightness += light.strength / d

            brightness = min(brightness, 1.0)

            c2 = (
                int(c[0] * brightness),
                int(c[1] * brightness),
                int(c[2] * brightness),
            )
        else:
            c2 = c
        #pg.gfxdraw.textured_polygon(window,((wallx[walls][0],wally[walls][0]),(wallx[walls][1],wally[walls][1]),(wallx[walls][3],wally[walls][3]),(wallx[walls][2],wally[walls][2])),image,0,0)
        draw(window,c2,((wallx[walls][0],wally[walls][0]),(wallx[walls][1],wally[walls][1]),(wallx[walls][3],wally[walls][3]),(wallx[walls][2],wally[walls][2])))
        
        

    
#math functions
def dist(x1,y1,x2,y2):
    return(M.sqrt(M.pow((x2-x1),2)+M.pow((y2-y1),2)))

def midp(x1,y1,x2,y2):
    return((x1 + x2) / 2, (y1 + y2) / 2)

def loadPlayerScripts(lines):
    SPEED = 100 #default speed value

    for line in lines:
        line = line.strip()

        if not line or line.startswith("*"):
            continue

        if line == "Done":
            break

        parts = line.split(maxsplit=1)

        key = parts[0]
        value = parts[1] if len(parts) > 1 else ""

        if key == "SHealth":
            HEALTH = int(value)

        elif key == "SSpeed":
            SPEED = float(value)

        elif key == "SCanRun":
            CanRun = value.startswith("T") #if its T then its true

        elif key == "SCanCrouch":
            CanCrouch = value.startswith("T")
            
    return SPEED, HEALTH, CanRun, CanCrouch



def loadObjectScripts(lines,NpcHandler):

    for line in lines:
        line = line.strip()

        if not line or line.startswith("*"):
            continue

        if line == "Done":
            break

        parts = line.split(maxsplit=1)

        key = parts[0]
        value = parts[1] if len(parts) > 1 else ""

        if line.startswith("NPC"):
            NpcHandler.npc_list.append(NPC(script=value))
        if line.startswith("LIGHT"):
            NpcHandler.light_list.append(LIGHT(script=value))



if __name__ == "__main__":
    main()

