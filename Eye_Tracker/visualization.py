import attr
from attr.validators import instance_of
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
# from PIL import Image
import seaborn as sns

@attr.s
class Visual:
    """Pipeline to visuaize the Eye tracker Data.
    Attributes: df, screen_res, cond_dict, ref_images.
    Methods: create_heatmap, plot.
    """
    df = attr.ib(validator=instance_of(pd.DataFrame))
    screen_res = attr.ib(validator=instance_of(tuple))
    cond_dict = attr.ib(validator=instance_of(dict))
    ref_images = attr.ib(validator=instance_of(dict))

    def create_heatmap(self, df_cond: pd.DataFrame, ref_img: str, ax) -> None:
        """Creates a heatmap over a ref_image, in a subplot on a spicifeid ax.
        The function as 2 steps:
        1. 2d histogram, using the screen resolotion
        2. heatmap over the image
        """
        # creating 2d density data: 2d histogram
        raw_x = df_cond['aveH'].to_numpy().ravel()
        raw_y = df_cond['aveV'].to_numpy().ravel()
        bins = [int(self.screen_res[0])/10, int(self.screen_res[1])/10] # devide by 10 for better visualization
        range_bins = [[0,int(self.screen_res[0])], [0,int(self.screen_res[1])]]
        data_2d, x_bin, y_bin = np.histogram2d(raw_x, raw_y, bins=bins, range=range_bins)
        
        # creating the heatmap over the image:
        heat = sns.heatmap(data_2d.T, cbar=True, cmap='Reds', alpha=0.5, zorder=2, ax=ax)
        map_img = mpimg.imread(ref_img)
        heat.imshow(map_img,
            aspect=heat.get_aspect(),
            extent=heat.get_xlim() + heat.get_ylim(),
            zorder=1, # put the map under the heatmap
            )

    def plot(self) -> None:
        """Makes large subplot to each condition"""
        cond_num = len(self.cond_dict)
        f, axes = plt.subplots(cond_num, 1, figsize=(16, 16), sharex=True, sharey=False)
        for ax, cond_key in zip(axes, self.cond_dict):
            df_cond = self.df[self.df['cond_int'] == self.cond_dict[cond_key]]
            try:
                ref_img = self.ref_images[cond_key]
            except KeyError:
                # should change to ask user input
                raise KeyError('reference images do not match experimental conditions.')
            self.create_heatmap(df_cond, ref_img, ax)
            ax.title.set_text(str(cond_key))
        # need to correct axes (*10), aspect ratio
        plt.show()


if __name__ == "__main__":
    pass