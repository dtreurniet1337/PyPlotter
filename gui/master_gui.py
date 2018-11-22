from tkinter import *

from gui.actions import Actions
from gui.tree import Tree

class MasterGUI:
    def __init__(self):
        print('GUI initialized')
        self.root = Tk()

        self.tree = Tree(self.root)

    def mainloop(self):
        self.tree.pack()
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def update_tree(self, tree):
        self.tree.update(tree)
