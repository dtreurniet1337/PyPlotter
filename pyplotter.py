# Created by Daan Treurniet
from gui.master_gui import MasterGUI
from datastore import DataStore

#gui = MasterGUI()

data_store = DataStore()
data_store.load_file('data/test_data_short.mat')
data_store.generate_tree()

#gui.mainloop()
