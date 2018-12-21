from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QGroupBox
from plotter_widgets.tree_view import TreeView

class FileBrowser(QGroupBox):
    def filter_changed(self):
        self.tree_view.update(filter = self.filter_textbox.text())

    def __init__(self, master):
        super().__init__()
        self.setTitle('File Browser')
        self.master = master

        self.filter_textbox = QLineEdit()
        self.filter_textbox.textChanged.connect(self.filter_changed)

        self.tree_view = TreeView(self.master)

        layout = QVBoxLayout()
        layout.addWidget(self.filter_textbox)
        layout.addWidget(self.tree_view)

        self.setLayout(layout)



    def update_tree(self): self.tree_view.update_tree()
