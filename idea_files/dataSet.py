from torch.utils.data import Dataset
import pandas as pd


class MyDataset(Dataset):
    def __init__(self, fileName, window):
        ohlcv = np.loadtxt(str(fileName), delimiter=",", dtype=np.float, skiprows=1, usecols=(1, 2, 3, 4, 5))
        self.data =
        self.window = window

    def __getitem__(self, index):
        x = self.data[index:index+self.window]
        return x

    def __len__(self):
        return len(self.data) - self.window
