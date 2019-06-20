import pandas as pd
import numpy as np

def gen_data():
    """ Creates mock data """
    times = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    con =   np.array([1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1])
    aveH =  np.array([2,4,2,6,10,15,14,3,7,8,10,15,10,10,10])
    aveV =  np.array([5,10,5,6,5,15,1,3,12,10,5,15,5,5,5])
    data = np.vstack([times, con, aveH, aveV]).T
    assert data.shape[1] == 4
    columns = ['time', 'condition', 'aveH', 'aveV']
    df = pd.DataFrame(data, columns=columns)
    df['ID'] = '345'
    df['design'] = 1
    df = df.set_index(['ID', 'design'])
    return df
