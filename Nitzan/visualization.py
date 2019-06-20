
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


def get_from_Goni():
    fix = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_fixations.csv')
    event = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_messages.csv')
    fix_obj = EyeFile(path=fix, fname=fix.name, id_num='01', design='1', data_type='fixations')
    event_obj = EyeFile(path=event, fname=event.name, id_num='01', design='1', data_type='events')

    data1 = IdData(fix_obj, event_obj)
    data1.run()

    fix2 = Path('CSV/FB/FB_integration_ID_02_design_2_time_04.11.18_13.32_fixations.csv')
    event2 = Path('CSV/FB/FB_integration_ID_02_design_2_time_04.11.18_13.32_messages.csv')
    fix_obj2 = EyeFile(path=fix2, fname=fix2.name, id_num='02', design='2', data_type='fixations')
    event_obj2 = EyeFile(path=event2, fname=fix2.name, id_num='02', design='2', data_type='events')

    data2 = IdData(fix_obj2, event_obj2)
    data2.run()
  
    big_data = AllId ([data1.df_id, data2.df_id])
    big_data.run()

    return big_data.df_all, big_data.cond_dict

def convert_to_png(fname_photo, new_name):
    jpg = Image.open (fname_photo) 
    png = jpg.save(new_name)
  
def make_heatmap(df, ph_png):
    #creeating 2d density data : 2d histogram
    raw_x = df['aveH'].to_numpy().ravel()
    raw_y = df['aveV'].to_numpy().ravel()
    bins = [1920/10,1080/10]
    range_bins = [[0,1920] , [0,1080]]
    data_2d, x_bin, y_bin = np.histogram2d(raw_x, raw_y, bins=bins, range = range_bins)
    
    #creating the heatmap over the picture:
    heat = sns.heatmap(data_2d.T,cbar = True, cmap = 'Reds', alpha = 0.5, zorder = 2)
    map_img = mpimg.imread(ph_png)
    
    heat.imshow(map_img,
          aspect = heat.get_aspect(),
          extent = heat.get_xlim() + heat.get_ylim(),
          zorder = 1) #put the map under the heatmap
        
    return heat

def super_grid(df,con_dict, pho_dict):
    con_num = len(con_dict)
    
    f, axes = plt.subplots(3, 2, figsize=(9, 9), sharex=True, sharey=True)
    
    for ax, con_ind in zip(axes.flat, con_dict):
        mask = df.loc['condition'] == con_ind
        df_cond = df.where(mask)
        cond_pho = pho_dict[con_ind] 
        make_heatmap(df_con,cond_pho )
    plt.show()

if __name__ == "__main__":
    
    df, cond_dict = get_from_Goni()
    # df = gen_data()
    # df = df.pop('con_wrd')
    # convert_to_png('FB_on_full_screen_Person.jpg', 'Person.png')
    # convert_to_png ('FB_on_full_screen_Face.jpg','Face.png')
    # make_heatmap(df,'Person.png')
    # super_grid(df,cond_dict,pho_dict)
    # plt.show()







