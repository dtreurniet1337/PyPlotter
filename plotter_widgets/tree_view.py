from PySide2.QtWidgets import QTreeView, QFileSystemModel
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import QDir

class TreeView(QTreeView):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.model = TreeModel(self.master)
        self.model.update()

        self.setModel(self.model)


class TreeModel(QStandardItemModel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.datastore = master.get_datastore()

    def update(self):
        self.clear()
        files = self.datastore.get_all_files()

        i = 0
        for filename, file in files.items():
            for name in file.get_names():
                print(name)
                self.setItem(i, 0, QStandardItem(name))
                i += 1
