from eye_GUI import *
from process_GUI_input import *
from read_data import *
from visualization import *

@attr.s
class EyeTracker:
    """Eye Tracker Analysis tool.
    Attributes: user_input, eyedict, df_list, b_data, visual.
    Methods:
    method input() prompts for user input.
    method rea_data() creates raw data objects for each file.
    method data() converts data of each trail to a pd.Dataframe.
    method big_data() creates one big pd.DataFrame from all data frames of a given experiment.
    method visualization() analyzes and outputs visualization of the experiment.
    method run() is the main function for this process.
    """
    user_input = attr.ib(default=eye_GUI)
    eyedict = attr.ib(default=attr.Factory(dict))
    df_list = attr.ib(default=attr.Factory(list))
    b_data = attr.ib(default=AllId)
    visual = attr.ib(default=Visual)
        
    def input(self) -> bool:
        """prompts for user input"""
        user_input = eye_GUI()
        assert_input = user_input.run()
        if not assert_input:
            return False
        self.user_input = user_input
        return True
    
    def raw_data(self) -> None:
        """creates raw data objects for each file"""
        filelist = ProcessFilelist(self.user_input.filelist)
        filelist.get_file_attrs()
        self.eyedict = filelist.eyedict

    def data(self) -> None:
        """creates data frame list"""
        for key, value in self.eyedict.items():
            fix_f, event_f = value.values()
            data = IdData(fix_f, event_f)
            data.run()
            self.df_list.append(data.df_id)
    
    def big_data(self) -> None:
        """creates one big data frame from all data frames in the list"""
        b_data = AllId (self.df_list)
        b_data.run()
        self.b_data = b_data

    def visualization(self) -> None:
        """analyzes and outputs visualization"""
        self.visual = Visual(self.b_data.df_all, self.user_input.screen_res, self.b_data.cond_dict, self.user_input.ref_images)
        self.visual.plot()

    def run(self) -> bool:
        """main function to run the process"""
        if not self.input():
            print('Cancelling...')
            return False
        print('Collecting files...')
        self.raw_data()
        print('Reading files...')
        self.data()
        print('Building dataframe...')
        self.big_data()
        print('Analyzing...')
        self.visualization()
        print('Done.')
        return True

if __name__ == "__main__":
    EyeTracker().run()