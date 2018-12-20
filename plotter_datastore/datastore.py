from parsers import intcanlog
import numpy as np


class DataStore:
    def __init__(self, plotter):
        self.plotter = plotter
        self.imported_files = {}

    def generate_tree(self):
        trees = []
        for file in self.imported_files.keys():
            tree = []
            subsystems_added = []
            id = 1
            data = self.imported_files[file]

            titles = data['title']
            # Dictionary to track if title has been added to tree
            title_added = {key: False for key in titles}

            # Find all systems
            systems = list(set([title.split('-')[0].strip() for title in titles]))
            # Sort alphabetically
            systems = sorted(systems, key=str.lower)
            # Add them to the tree
            for name in systems:
                tree.append((id, name, 0))
                id += 1

            # Make copy to iterate over system names
            tree_systems = tree.copy()
            # Start filling the tree with subsystems
            for branch in tree_systems:
                system = branch[1]

                # Look for 2 word recurring pattern
                reg = re.compile(re.escape(system) + r'.*')
                matches = list(filter(reg.match, titles))
                for match in matches:
                    # If the group is smaller than 5, it is not a subsystem
                    if len(match.split()) < 4:
                        continue

                    # Found a subsystem. Now find all datasets that belong to it
                    subsystem = ' '.join(match.split()[2:4])
                    reg = re.compile(re.escape(system) + r' - ' + re.escape(subsystem))
                    matches_2word = sorted(list(filter(reg.match, titles)), key=str.lower)

                    # Group together if 4 or more occurences are found
                    if len(matches_2word) >= 4:
                        if subsystem not in subsystems_added:
                            # Add subsystem branch to the tree in the system branch
                            subsystems_added.append(subsystem)
                            tree.append((id, subsystem, branch[0]))
                            subsystem_id = id
                            id += 1
                            # Sort matches before adding them
                            for title in matches_2word:
                                # Add the datasets in the right subsystem branch
                                tree.append((id, ' '.join(title.split()[4:]), subsystem_id))
                                id += 1
                                title_added[title] = True

                # Look for 1 word recurring pattern
                titles_left = [title for title in titles if title_added[title] == False]
                reg = re.compile(re.escape(system) + r'.*')
                matches = list(filter(reg.match, titles_left))
                for match in matches:
                    # If the group is smaller than 5, it is not a subsystem
                    if len(match.split()) < 4:
                        continue

                    # Found a subsystem. Now find datasets that belong to it
                    subsystem = ' '.join(match.split()[2:3])
                    reg = re.compile(re.escape(system) + r' - ' + re.escape(subsystem) + r' ')
                    matches_2word = sorted(list(filter(reg.match, titles_left)), key=str.lower)

                    # If there is less than 4 recurring titles, don't group them
                    if len(matches_2word) < 4:
                        continue
                    # Else, group them in a subsystem folder
                    else:
                        if subsystem not in subsystems_added:
                            subsystems_added.append(subsystem)
                            tree.append((id, subsystem, branch[0]))
                            subsystem_id = id
                            id += 1
                            for title in matches_2word:
                                if not title_added[title]:
                                    tree.append((id, ' '.join(title.split()[3:]), subsystem_id))
                                    id += 1
                                    title_added[title] = True

                # Add remaining titles for this system
                titles_left = [title for title in titles if title_added[title] == False]
                reg = re.compile(re.escape(system) + r'.*')
                matches = sorted(list(filter(reg.match, titles_left)), key=str.lower)
                for title in matches:
                    name = ' '.join(title.split()[2:])
                    tree.append((id, name,branch[0]))
                    id += 1
                    title_added[title] = True

            trees.append(tree)

        return trees






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
