from CybrocksLibrary import *
import base64
import random as R

petI = None

def init(data):
    global petI
    print('hi')
    image = base64.b64decode(b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAkklEQVQ4je2SKxKAMAxEl0xPEYfGIREcHlGJQ+N6CqbF8EloCsxgWUUL+7JLC/z6rKr4htqk1nE0v3UlI8dGbQdCskAaQG2SxtD1xzN7ARIQKpmv2mEcG1WPig4A7AcTokLL6bXxS0ywSJElqOEU6CnFbYU3Oo/EqDFjySazHxBoOo4zKy1NUtcqeYItxavc4h6s1Gs0zvcqAy0AAAAASUVORK5CYII=')

    petI = BetterImage(image, (R.randrange(0,data['RESx']-16), data['RESy']-16), 1, 1)
def update():
    pass


def draw(window):
    if petI is not None:
        petI.draw(window)