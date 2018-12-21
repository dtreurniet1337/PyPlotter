from parsers import intcanlog
import numpy as np


class DataStore:
    def __init__(self, plotter):
        self.plotter = plotter
        self.imported_files = {}

    def load_file(self, filename, track_time = False):
        if filename in self.imported_files:
            print('Warning: overwriting %s' % filename)
        data = intcanlog.load_file(filename, track_time)
        self.imported_files[filename] = data

    def get_file(self, filename):
        if self.imported_files[filename]: return self.imported_files[filename]
        else:
            raise IndexError('Requested filename not in datastore')

    def get_all_files(self):
        return self.imported_files
