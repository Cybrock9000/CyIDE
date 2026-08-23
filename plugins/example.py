


#settingsdata contains everything from settings.json
def init(settingsdata): # some vars dont init right away so you have to set them here, see CyIDEExtras for example
    print('loaded example')
    

#                                                                                                \/ colors \/
#idedata contains (in order) scrolly, scrollx, len(code), keys, clock.get_fps(), font, (tab,tab1,tab2,tab3,margin,text1), data
def update(idedata):
    pass

def draw(window): #draw on top of everything but the panel
    pass

def drawpanel(window): #draw on top of panel but only when panel is out
    pass

def drawoverlay(window): #draw on top of everything
    pass