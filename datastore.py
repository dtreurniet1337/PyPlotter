import matplotlib.pyplot as plt
from parsers import intcanlog

class DataStore:
    def __init__(self):
        print('Data Store initialized')
        self.imported_files = {}

    def generate_tree(self):
        for file in self.imported_files.keys():
            data = self.imported_files[file]

            # Generate a list of all dataset titles as a list split by spaces
            datasets = [title.split() for title in list(data['title'])]

            categories = []
            # First split by categorizing to the - character
            for title_index, title in enumerate(datasets):
                for word_index, word in enumerate(title):
                    if word == '-':
                        if title[:word_index] not in categories:
                            categories.append(title[:word_index])
            print(categories)


    def load_file(self, filename, track_time = False):
        if filename in self.imported_files:
            print('Warning: overwriting %s' % filename)
        data = intcanlog.load_file(filename, track_time)
        self.imported_files[filename] = data
