
#importing packages:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from params import *

# calling the data
from multiindex_file import gen_data

if __name__ == "__main__":
    df = gen_data()

    raw_x = df['aveV'].to_numpy().ravel()
    raw_y = df['aveH'].to_numpy().ravel()
    data_2d, bins_x, bins_y = np.histogram2d(raw_x, raw_y, bins=15)
    fig, ax = plt.subplots()
    ax.imshow(data_2d, cmap='gray')
    plt.show()

