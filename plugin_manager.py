import os
import importlib
import json



class pluginM:
    def __init__(self):
        with open('plugins/disabledPlugins.txt', "r") as f:
            blacklist = f.read()
        self.pluginsloaded = []
        for filename in os.listdir('plugins/'):
            print(filename)
            if filename.endswith(".py"):
                if not filename[:-3] in blacklist:
                    plugin = importlib.import_module(f"plugins.{filename[:-3]}")
                    self.pluginsloaded.append(plugin)
                    print(self.pluginsloaded)

    def init(self,data):
        for plugin in self.pluginsloaded:
            plugin.init(data)
    def update(self):
        for plugin in self.pluginsloaded:
            plugin.update()

    def draw(self,window):
        for plugin in self.pluginsloaded:
            plugin.draw(window)


    def add_plugin(self, plugin):
        self.pluginsloaded.append(plugin)