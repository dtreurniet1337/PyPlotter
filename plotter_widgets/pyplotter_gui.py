from PySide2.QtWidgets import QWidget, QHBoxLayout

import plotter_widgets

class PyplotterGui(QWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.file_browser = plotter_widgets.FileBrowser(self.master)

        layout = QHBoxLayout()
        layout.addWidget(self.file_browser)

        self.setLayout(layout)
