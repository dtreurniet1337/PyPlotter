import numpy as np
from numpy.lib import recfunctions
import scipy.io as sio
import uid_tools
from helpers import TimeTracker
import matplotlib.pyplot as plt

class DataStore:
    def __init__(self):
        print('Data Store initialized')
        self.time_tracker = TimeTracker(print_process=True)
        self.imported_files = []


    def __simplify_list(self, lst):
        """
        Recursive function to simplify a nested list to the most basic form.
        The nested list can have unknown depth and unknown content.
        In case of a single value, it will return a single value.
        In case of a list with more values, it will return a simple list.

        :param lst: list to simplify
        :return: lowest level object
        """
        list_obj = [list, np.ndarray]

        # Check if current lst is a list or array. If not, return it
        if type(lst) not in list_obj:
            return lst
        # lst is a list, so check if there is something in it. If not, return None
        elif lst.size == 0:
            return None
        # lst is a list with something in it. Go down recursively
        else:
            return self.__simplify_list(lst[0])

    def load_file(self, file, dataset_selection=None, track_time=False):
        print('\nLoading file %s' % (file))
        self.time_tracker.tic()

        raw_data = sio.loadmat(file)
        self.time_tracker.toc('Load MAT file')

        # Determine number of messages
        n_messages = raw_data['messages'].shape[1]

        # Get IDs from the raw data
        message_ids = np.reshape(np.transpose(raw_data['messages'][0:2, :]), 2*n_messages)
        # Convert from uint8 to uint16 to obtain IDs
        message_ids.dtype = np.uint16
        self.time_tracker.toc('Convert IDs')

        # Get timestamps from the raw data
        message_dt = np.reshape(np.transpose(raw_data['messages'][2:4, :]), 2*n_messages)
        message_dt.dtype = np.int16
        # Convert from dt values to absolute timestamps
        message_timestamps = 0.001*np.cumsum(message_dt)
        self.time_tracker.toc("Convert timestamps")

        # Filter datasets with plot-able datatypes
        datasets = raw_data['datasets'][raw_data['datasets']['datatype'] <= 9]
        n_datasets = datasets.shape[0]
        print('%s datasets found' % (n_datasets))

        # Run through the dataset and convert 1x1 numpy arrays to normal datatypes
        for field in datasets.dtype.names:
            for i in range(len(datasets[field])):
                datasets[field][i] = self.__simplify_list(datasets[field][i])
        self.time_tracker.toc("Simplify numpy arrays")

        # Check whether UIDs are already present in dataset. If not, generate them
        if 'uid' not in datasets.dtype.names:
            print('No UID found. Performing look-up')

            # Generate UID list with generator expression using encoding function of uid_tools
            uids = np.fromiter((uid_tools.encode(datasets['name'][i]) for i in range(datasets.shape[0])), dtype=np.uint32)

            # Append UID field to existing datasets structured array
            datasets = recfunctions.append_fields(datasets, 'uid', uids)
        self.time_tracker.toc("Generate UIDs")

        # If a dataset_selection is given, only select these
        if dataset_selection:
            pass

        # Count number of messages per dataset
        datasets_to_keep = np.zeros((n_datasets, 1), dtype=np.bool_)
        messages_per_dataset = np.zeros((n_datasets, 1), dtype=np.uint16)
        for i in range(n_datasets):
            non_zero_messages = np.count_nonzero(message_ids == datasets[i]['id'])
            if non_zero_messages > 0:
                datasets_to_keep[i] = True
                messages_per_dataset[i] = non_zero_messages
        datasets = datasets[np.squeeze(datasets_to_keep)]
        messages_per_dataset = messages_per_dataset[datasets_to_keep]
        self.time_tracker.toc("Remove empty datasets")
        print("%s empty datasets removed"%(n_datasets - datasets.shape[0]))
        n_datasets = datasets.shape[0]

        # Create data vector
        data_dtype = np.dtype({'names': ['source', 'title', 'UID',
                                         'xData', 'xQuantity', 'xUnit',
                                         'yData', 'yQuantity', 'yUnit',
                                         'startTime'],
                               'formats': ['U2', 'U64', 'i4',
                                           np.object_, 'U64', 'U64',
                                           np.object_, 'U64', 'U64',
                                           'f8']})
        data = np.zeros(n_datasets, dtype=data_dtype)

        # Populate data array
        for i in range(n_datasets):
            data[i]['source'] = 'SD'
            data[i]['title'] = datasets[i]['name']
            data[i]['UID'] = datasets[i]['uid']
            data[i]['xData'] = np.zeros(messages_per_dataset[i], dtype=np.float64)
            data[i]['xQuantity'] = 'time'
            data[i]['xUnit'] = 's'
            data[i]['yData'] = np.zeros(messages_per_dataset[i], dtype=np.float64)
            data[i]['yQuantity'] = datasets[i]['quantity']
            data[i]['yUnit'] = datasets[i]['unit']

            # Populate xData
            message_indices = np.nonzero(message_ids == datasets[i]['id'])[0]
            data[i]['xData'] = message_timestamps[message_indices]

            # Populate yData
            ls_byte = datasets[i]['byte_offset'] + 4  # index where data starts
            ms_byte = ls_byte + datasets[i]['length']  # index where data ends
            raw_ydata = np.squeeze(raw_data['messages'][ls_byte:ms_byte, message_indices])

            # Convert data to the correct datatype
            datatype = datasets[i]['datatype']
            if datatype == 0:
                data[i]['yData'] = raw_ydata
            elif datatype == 1:
                raw_ydata.dtype = np.int8
                data[i]['yData'] = raw_ydata
            elif datatype == 2:
                raw_ydata.dtype = np.uint16
                data[i]['yData'] = raw_ydata
            elif datatype == 3:
                raw_ydata.dtype = np.int16
                data[i]['yData'] = raw_ydata
            elif datatype == 4:
                raw_ydata.dtype = np.uint32
                data[i]['yData'] = raw_ydata
            elif datatype == 5:
                raw_ydata.dtype = np.int32
                data[i]['yData'] = raw_ydata
            elif datatype == 6:
                raw_ydata.dtype = np.uint64
                data[i]['yData'] = raw_ydata
            elif datatype == 7:
                raw_ydata.dtype = np.int64
                data[i]['yData'] = raw_ydata
            elif datatype == 8:
                raw_ydata.dtype = np.float32
                data[i]['yData'] = raw_ydata
            elif datatype == 9:
                raw_ydata.dtype = np.float64
                data[i]['yData'] = raw_ydata

            # Apply offset and scaling
            data[i]['yData'] = datasets[i]['offset'] + datasets[i]['scale']*data[i]['yData']

            # Remove duplicates
            data[i]['xData'] = np.unique(data[i]['xData'])
            data[i]['yData'] = np.unique(data[i]['yData'])

        self.time_tracker.toc('Populating data')
