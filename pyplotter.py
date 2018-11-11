# Created by Daan Treurniet

from datastore import DataStore

data_store = DataStore()

data_store.load_file('data/test_data_short.mat', track_time=True)
