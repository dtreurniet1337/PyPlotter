
class DataFile:
    def __init__(self, filename):
        self.filename = filename.split('/')[-1]
        self.names = []
        self.raw_data = []

    def get_names(self): return self.names
    def get_filename(self): return self.filename
