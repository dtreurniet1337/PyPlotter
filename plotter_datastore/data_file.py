
class DataFile:
    def __init__(self, filename):
        self.filename = filename
        self.names = []
        self.raw_data = []

    def get_names(self): return self.names
