import tkinter.ttk as ttk

class Tree(ttk.Treeview):
    def __init__(self, master):
        super().__init__()
        self.master = master

    def update(self, tree):
        last_branch = ''
        for branch in tree:
            if type(branch) == list:
                for leaf in branch:
                    self.insert(last_branch, 'end', text=leaf)
            else:
                self.insert('', 'end', branch, text=branch)
                last_branch = branch
