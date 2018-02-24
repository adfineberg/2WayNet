import os

import pandas as pd

from MISC.container import ContainerRegisterMetaClass
from .dataset_base import DatasetBase


class ProteinAtlas(object):
    def __init__(self, path='.'):
        self.path = path
        self.data = []

    def load(self):
        location = pd.read_csv(os.path.join(self.path, 'loc.csv')).sort_values(by='ENSG').select_dtypes(include=['int64'])
        mrna_filtered = pd.read_csv(os.path.join(self.path, 'mrna-filter.csv')).sort_values(by='ENSG').select_dtypes(include=['float64'])

        return location.values, mrna_filtered.values

    @classmethod
    def display(cls, img, width=28, threshold=200):
        render = ''
        for i in range(len(img)):
            if i % width == 0: render += '\n'
            if img[i] > threshold:
                render += '@'
            else:
                render += '.'
        return render


class ProteinAtlasDataSet(DatasetBase):
    __metaclass__ = ContainerRegisterMetaClass

    def __init__(self, data_set_parameters):
        super(ProteinAtlasDataSet, self).__init__(data_set_parameters)

    def build_dataset(self):
        protein_atlas = ProteinAtlas(self.dataset_path)
        data_set_x, data_set_y = protein_atlas.load()

        data_set_x, test_set_x, test_samples = self.produce_optimization_sets(data_set_x)
        data_set_y, test_set_y, test_samples = self.produce_optimization_sets(data_set_y, test_samples)

        train_set_x, tuning_set_x, test_samples = self.produce_optimization_sets(data_set_x)
        train_set_y, tuning_set_y, test_samples = self.produce_optimization_sets(data_set_y, test_samples)

        self.trainset = train_set_x, train_set_y
        self.tuning = tuning_set_x, tuning_set_y
        self.testset = test_set_x, test_set_y
