# Created by Daan Treurniet
import sys
from PySide2 import QtWidgets

import plotter_widgets
import plotter_datastore

class PyPlotter():
    def __init__(self):
        self.data_store = plotter_datastore.DataStore(self)
        self.data_store.load_file('data/test_data_short.mat')

        self.app = QtWidgets.QApplication([])
        self.main_gui = plotter_widgets.PyplotterGui(self)

        self.main_gui.show()

        sys.exit(self.app.exec_())

    def get_datastore(self): return self.data_store

if __name__ == '__main__':
    pyplotter = PyPlotter()
