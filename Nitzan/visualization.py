
#importing packages:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path
from PIL import Image
import matplotlib.image as mpimg


from params import *
from multiindex_file import gen_data
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

def get_2d(df):
    raw_x = df['aveH'].to_numpy().ravel()
    raw_y = df['aveV'].to_numpy().ravel()
    bins = [1080/10, 1920/10]
    data_2d, x_bin, y_bin = np.histogram2d(raw_x, raw_y, bins=bins)
    return data_2d

def convert_to_png(fname_photo, new_name):
    jpg = Image.open (fname_photo) 
    png = jpg.save(new_name)
    
def make_heat(data_2d, ph_png):
    heat = sns.heatmap(data_2d,cbar = True, cmap = 'Reds', alpha = 0.5, zorder = 2)
    map_img = mpimg.imread(ph_png)
    
    heat.imshow(map_img,
          aspect = heat.get_aspect(),
          extent = heat.get_xlim() + heat.get_ylim(),
          zorder = 1) #put the map under the heatmap
    
    plt.show()
    
    return heat

if __name__ == "__main__":
    
    df= get_from_Goni()
    # df = gen_data()
    data_2d= get_2d(df)
    convert_to_png('FB_on_full_screen_Person.jpg', 'Person.png')
    make_heat(data_2d,'Person.png')
    # fig, ax = plt.subplots()
    # ax.imshow(data_2d, cmap='gray')






