from read_data import *
from visualization import *
from process_GUI_input import *
from eye_GUI import *

# yossi
class EyeTracker:
    def __init__(self):
        self.df_list = []
        pass

# goni
    def data(self):
        """ creates data frame list"""
        for key, value in f.eyedict:
            fix_f, event_f = value.values
            data = IdData(fix_f, event_f)
            data.run()
            self.df_list.append(data.df_id)
    
    def big_data(self):
         """ create one big data frame from all data frames in the list """
        b_data = AllId (self.df_list)
        b_data.run()

    

    def run (self):
        self.data()



