from read_data import *
from visualization import *
from process_GUI_input import *
from eye_GUI import *

# yossi
class EyeTracker:
    def __init__(self):
        self.df_list = []
        
    def input(self):
        """prompts for user input"""
        user_input = eye_GUI()
        user_input.run()
        self.user_input = user_input
    
    def raw_data(self):
        """creates raw data objects for each file"""
        filelist = ProcessFilelist(self.user_input.filelist)
        filelist.get_file_attrs()
        self.eyedict = filelist.eyedict

# goni
    def data(self):
        """ creates data frame list"""
        for key, value in self.eyedict.items():
            fix_f, event_f = value.values()
            data = IdData(fix_f, event_f)
            data.run()
            self.df_list.append(data.df_id)
    
    def big_data(self):
        """ create one big data frame from all data frames in the list """
        b_data = AllId (self.df_list)
        b_data.run()
        self.b_data = b_data

# nitzan
    def visual(self):
        visualization = Visual(self.b_data.df_all, self.user_input.screen_res, self.b_data.cond_dict, self.user_input.ref_images)
        visualization.run()

    def run(self):
        self.input()
        self.raw_data()
        self.data()
        self.big_data()
        self.visual()

if __name__ == "__main__":
    EyeTracker().run()