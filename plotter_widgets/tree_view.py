from PySide2.QtWidgets import QTreeView, QFileSystemModel, QAbstractItemView
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import QDir

import re

class TreeView(QTreeView):
    def __init__(self, master):
        super().__init__()
        self.master = master

        # Set selection mode so multiple datasets can be selected
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # Hide header
        self.setHeaderHidden(True)

        self.model = TreeModel(self.master)
        self.model.update()
        self.setModel(self.model)

    def update(self, filter = None):
        self.model.update(selection_reg = filter)



class TreeModel(QStandardItemModel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.datastore = master.get_datastore()

    def update(self, selection_reg=None):
        # Empty the model to start fresh
        self.clear()

        # Get loaded files from datastore
        files = self.datastore.get_all_files()

        # Iterate over files in datastore and build model
        for key, file in files.items():
            # Add filename to model
            parentItem = self.invisibleRootItem()
            item_file = TreeItem(file.get_filename())
            parentItem.appendRow(item_file)

            # Get list of dataset names in file
            dataset_names = file.get_names()

            # If a selection regex is given, filter all datasets with it
            if selection_reg:
                reg = re.compile(r'{}'.format(selection_reg))
                dataset_names = list(filter(reg.match, dataset_names))

            # Create dict to keep track of a dataset has been added to the tree
            dataset_added = {key: False for key in dataset_names}
            # Create list to keep track of added subsystems
            subsystem_added = []

            # Find all systems in the file and sort them
            dataset_systems = list(set([name.split('-')[0].strip() for name in dataset_names]))
            dataset_systems = sorted(dataset_systems, key=str.lower)

            # Add systems to the model
            for system in dataset_systems:
                # Select file item to start building model for this file
                parentItem = item_file

                # Create an item for this system and make it the root
                item_system = TreeItem(system)
                parentItem.appendRow(item_system)

                # Get all datasets that belong to this system
                reg = re.compile(re.escape(system) + r'.*')
                system_datasets = list(filter(reg.match, dataset_names))

                # Iterate over all datasets belonging to this system
                for dataset in system_datasets:
                    # Select system item as parentItem
                    parentItem = item_system

                    # Look for subsystems with 2 words in common
                    subsystem = ' '.join(dataset.split()[:4])
                    reg = re.compile(re.escape(subsystem))
                    subsystem_datasets = sorted(list(filter(reg.match, dataset_names)), key=str.lower)

                    # Only if subsystem has more than 2 datasets, it is grouped in a subsystem-folder
                    if len(subsystem_datasets) > 2 and subsystem not in subsystem_added:
                        # Add this subsystem to the list to prevent adding it again
                        subsystem_added.append(' '.join(dataset.split()[:4]))

                        # Add this subsystem to the model
                        item_subsystem = TreeItem(' '.join(subsystem.split()[2:4]))
                        parentItem.appendRow(item_subsystem)

                        # Add all datasets that belong to the subsytem to the model
                        parentItem = item_subsystem
                        for subsytem_dataset in subsystem_datasets:
                            item_dataset = TreeItem(' '.join(subsytem_dataset.split()[4:]))
                            parentItem.appendRow(item_dataset)
                            dataset_added[subsytem_dataset] = True

                    # Remove already-added datasets from the list to avoid double entries
                    dataset_names = [name for name in dataset_names if dataset_added[name] == False]

                    # Select system item as parentItem
                    parentItem = item_system

                    # Look for subsystems with 1 words in common
                    subsystem = ' '.join(dataset.split()[:3])
                    reg = re.compile(re.escape(subsystem))
                    subsystem_datasets = sorted(list(filter(reg.match, dataset_names)), key=str.lower)

                    # Only if subsystem has more than 3 datasets, it is grouped in a subsystem-folder
                    if len(subsystem_datasets) > 2 and subsystem not in subsystem_added:
                        # Add this subsystem to the list to prevent adding it again
                        subsystem_added.append(' '.join(dataset.split()[:3]))

                        # Add this subsystem to the model
                        item_subsystem = TreeItem(' '.join(subsystem.split()[2:3]))
                        parentItem.appendRow(item_subsystem)

                        # Add all datasets that belong to the subsytem to the model
                        parentItem = item_subsystem
                        for subsytem_dataset in subsystem_datasets:
                            item_dataset = TreeItem(' '.join(subsytem_dataset.split()[3:]))
                            parentItem.appendRow(item_dataset)
                            dataset_added[subsytem_dataset] = True

                # Get remaining datasets and add them
                dataset_names = [name for name in dataset_names if dataset_added[name] == False]
                parentItem = item_system
                for system_dataset in system_datasets:
                    if dataset_added[system_dataset] == False:
                        item_dataset = TreeItem(' '.join(system_dataset.split()[2:]))
                        parentItem.appendRow(item_dataset)


class TreeItem(QStandardItem):
    def __init__(self, label):
        super().__init__(label)
