
#importing packages:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path
from PIL import Image
import matplotlib.image as mpimg

class Visual (self, df, reso, cond_dict, pho_dict):
    ''' Visuaize the Eye tracker Data
    '''

    def __init__ (self):
        self.df = df
        self.reso = reso
        self.cond_dict = cond_dict
        self.pho_dict = pho_dict
        
    def convert_to_df_not_object(self):
        '''
        takes out the condition as string, leaving only the integer part.
        then, changes the DF to not be object.
        '''
        self.df.pop('condition')
        self.df = self.df.infer_objects()

    def make_heatmap(self, ph_png,ax):
        '''
        creates a heatmap over the photo in the speceafied file name in ph_png.       
        then, puts it in the spicifeid ax (to be a sbplot)
        the function as 2 steps: 
        1. 2 d histogram, using the resolotion (devided by 10 for better visualize)
        2. heatmap over the map
        '''

        #creating 2d density data : 2d histogram
        raw_x = self.df['aveH'].to_numpy().ravel()
        raw_y = self.df['aveV'].to_numpy().ravel()
        bins = [self.reso[0]/10,self.reso[1]/10] #change to tuple
        range_bins = [[0,self.reso[0]] , [0,self.reso[1]]]
        data_2d, x_bin, y_bin = np.histogram2d(raw_x, raw_y, bins=bins, range = range_bins)
        
        #creating the heatmap over the picture:
        heat = sns.heatmap(data_2d.T,cbar = True, cmap = 'Reds', alpha = 0.5, zorder = 2, ax=ax)
        
        map_img = mpimg.imread(ph_png)
        
        heat.imshow(map_img,
            aspect = heat.get_aspect(),
            extent = heat.get_xlim() + heat.get_ylim(),
            zorder = 1, #put the map under the heatmap
            ) 
            
        return heat

    def super_grid(self):
        ''' makes large subplot to each condition 
        '''

        con_num = len(self.cond_dict)
        
        f, axes = plt.subplots(con_num, 1, figsize=(16, 16),sharex = True, sharey=False)
        
        for ax, cond_key in zip(axes, self.cond_dict):
            df_cond = df.loc[lambda self.df:self.df['cond_int'] == self.cond_dict[cond_key]]
            cond_pho = self.pho_dict[cond_key]
            self.make_heatmap(df_cond,cond_pho,ax)
            ax.title.set_text(str(cond_key))

        plt.show()

    def run(self):
        '''main pipeline'''
        self.convert_to_df_not_object()
        self.super_grid()        



if __name__ == "__main__":
    pass
    
