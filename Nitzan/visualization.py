
#importing packages:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path
import matplotlib.image as mpimg

from params import *

from read_data_new import *
# go be removed later:

def get_from_Goni():
    fix = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_fixations.csv')
    event = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_messages.csv')
    fix_obj = EyeFile(path=fix, fname=fix.name, id_num='01', design='1', data_type='fixations')
    event_obj = EyeFile(path=event, fname=fix.name, id_num='01', design='1', data_type='events')
    data1 = ProcessData(fix_obj, event_obj)
    df = data1.convert_fixations_to_df() 
    df = data1.df_fixations
    return df

def get_2d():
    raw_x = df['aveH'].to_numpy().ravel()
    raw_y = df['aveV'].to_numpy().ravel()
    bins = [1080/10,1920/10]
    data_2d, bins_x, bins_y = np.histogram2d(raw_x, raw_y, bins=bins)
    return data_2d

def make_padle(df):
    raw_x = df['aveH'].to_numpy().ravel()
    raw_y = df['aveV'].to_numpy().ravel()
    sns.kdeplot(raw_x, raw_y)
    



if __name__ == "__main__":
    
    df= get_from_Goni()
    data_2d= get_2d()
    con_image = mpimg.imread(fname_photo)
    padle = make_padle(df)
    fig, ax = plt.subplots()
    ax.imshow(padle, cmap='gray')
    plt.show()






