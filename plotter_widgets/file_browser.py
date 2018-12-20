from PySide2.QtWidgets import QWidget, QHBoxLayout
from plotter_widgets.tree_view import TreeView

class FileBrowser(QWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.tree_view = TreeView(self.master)

        layout = QHBoxLayout()
        layout.addWidget(self.tree_view)

        self.setLayout(layout)



    def update_tree(self): self.tree_view.update_tree()
