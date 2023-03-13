"""
Class that contains scattering data
"""
import numpy as np
import pandas as pd

class ScatterData:
    def __init__(self, file=None):
        if file is None:
            self.q = np.zeros(1)
            self.i = np.zeros(1)
            self.error = []

        else:
            self.parse(file)

    def parse(self, file):
        """
        Parses scattering data into numpy arrays and
        stores withing class object

        Parameters
        ----------
        file : csv file containing three columns with:
         scattering vector, q
         scattering Intensity, I
         experimental error, e

        """
        df = pd.read_csv(file, names=['q', 'I1', 'I2'], index_col=False, sep=',')
        self.q = df['q'].to_numpy()
        self.i = df['I1'].to_numpy()
        self.error = df['I2'].to_numpy()

    def set_data(self, q, i, e=None):
        """
        Sets scattering data manually from arrays or
        likewise instead of file

        Parameters
        ----------
        q : np.array
        i : np.array
        e : np.array (optional)
        """
        if e is None:
            e = []
        self.q = q
        self.i = i
        self.error = e

    def cut_q(self, q_min, q_max):
        indices = np.logical_and(q_min <= self.q, self.q <= q_max)
        q = self.q[indices]
        i = self.i[indices]
        if self.error != []:
            error = self.error[indices]
        else:
            error = []
        copy = ScatterData()
        copy.set_data(q, i, error)
        return copy

    def scale_intensity(self, factor):
        copy = ScatterData()
        scaled_intensity = factor * self.i
        copy.set_data(self.q, scaled_intensity, self.error)
        return copy

    def scale_q(self, factor):
        copy = ScatterData()
        scaled_q = factor * self.q
        copy.set_data(scaled_q, self.i, self.error)
        return copy
