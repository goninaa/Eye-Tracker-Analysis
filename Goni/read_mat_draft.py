import numpy as np
import pandas as pd
import scipy.io as sio
from datetime import datetime, timedelta

def mat_to_py_time(matlab_datenum):
    python_datetime = datetime.fromordinal(int(matlab_datenum)) + timedelta(days=matlab_datenum%1) - timedelta(days = 366)
    return python_datetime

class Data:

    def __init__(self, fname):
        self.fname = fname
        self.df = None

    def mat_to_df(self):
        mat = sio.loadmat(self.fname)
        pass





if __name__ == "__main__":

    fname = 'FB_integration_ID_01_design_1_time_04.11.18_11.43.mat' 
    mat = sio.loadmat(fname)   
    who = sio.whosmat (fname)
    # print (mat.items())
    # keys = (sorted(mat.keys()))
    data_mat = mat['edf_data']
    fixations = mat['edf_data']['fixations'][()]
    messages = mat['edf_data']['messages'][()]
    start_fix = fixations[0,0]['startTime'][0,0]
    end_fix = fixations[0,0]['endTime'][0,0]
    ave_h_fix = fixations[0,0]['aveH'][0,0]
    ave_v_fix = fixations[0,0]['aveV'][0,0]
    message = messages[0,0]['message'][0,0]
    time_msg = messages[0,0]['time'][()]
  
    print (message)

    """mat['S']['b'][()][0,3]
which will access the data value in the 0th row, 
3rd column of the field named 'b' in the structure named 'S' 
in the Matlab data loaded into 'mat'."""