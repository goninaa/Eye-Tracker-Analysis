import pandas as pd
import attr
from attr.validators import instance_of
from mock_EyeFile_pair import *
from collections import defaultdict
import time

class IdData:
    """ Pipeline to process data of one ID on one design
    (both fixations and conditions)"""
    def __init__(self, fixations, events):
        self.fixations = pd.read_csv(fixations.path)
        self.events = pd.read_csv(events.path)
        self.id_num = fixations.id_num
        self.design = fixations.design
        self.df_fixations = None
        self.df_cond = None
        self.df_id = None

    def create_fixation_df (self):
        """ convert fixations file to data frame """          
        df = self.fixations.copy()
        df['ID'] = self.id_num
        df['design'] = self.design
        time_periods = pd.DataFrame({'time': pd.RangeIndex(start = df.startTime.min(), stop = df.endTime.max())}) #create all time-stamps
        df = time_periods.merge(df, how='left', left_on='time', right_on='startTime').fillna(method='pad') #merge
        mask = (df['time'] >= df['startTime']) & (df['time'] <= df['endTime'])
        df = df.where(mask)
        df = df.dropna()
        df.pop('startTime')
        df.pop('endTime')
        self.df_fixations = df

    def create_cond_df (self):
        """ create conditions data frame """
        df = self.events.copy()
        start = df.loc[df.loc[:, 'message'].str.contains('BLOCK_START'), :]
        end = df.loc[df.loc[:, 'message'].str.contains('STIM_DISP_END'), :]
        df = df.loc[~df.loc[:, 'message'].str.contains('BLOCK_END'), :]
        df['start'] = start.loc[:, 'time']
        df['end'] = end.loc[:, 'time']
        df['condition'] = df.loc[:, 'message'].str.split(':').str[2].str.strip()
        df = df.fillna(method= 'pad')
        df = df.rename(index=str, columns={"time": "orignal_time"})
        time_periods = pd.DataFrame({'time': pd.RangeIndex(start = df.start.min(), stop = df.end.max())})
        df = time_periods.merge(df, how='left', left_on='time', right_on='start').fillna(method='pad') 
        mask = (df['time'] >= df['start']) & (df['time'] <= df['end'])
        df = df.where(mask)
        df = df.dropna()
        df.pop('orignal_time')
        df.pop('start')
        df.pop('end')
        df.pop('message')
        df['cond_int'] = df['condition']
        self.df_cond = df

    def merge_df (self):
        """ merge conditions and fixations dataframes into one multi-index
        data frame, with ID and design """
        df = self.df_fixations.merge(self.df_cond, on = 'time')
        df = df.dropna()
        self.df_id = df
        self.df_id = df.set_index(['ID', 'design'])

    def run (self):
        """ main pipeline """
        self.create_fixation_df()
        self.create_cond_df()
        self.merge_df()
    
class AllId:
    """ data frame of all IDs designs.
    from several IdData. gets list of  """
    def __init__(self,df_list):
        self.df_list = df_list
        self.df_all = None
        self.cond_dict = {}
        self.df_merge = None

    def merge_df (self, basic_df, df) :
        """ merge IdData into one multi-index
        data frame """
        df_merge = pd.concat ([basic_df, df])
        df_merge = df_merge.dropna()
        self.df_merge = df_merge
        return df_merge

    def create_big_data(self):
        """ merge all data frames in the list 
        into one big data frame"""
        basic_df = self.df_list.pop(0)
        for df in self.df_list:
            basic_df = self.merge_df(basic_df,df)
        self.df_all = basic_df

    def cond_names (self):
        """ replace all conditions names in 'cond_int' column into int"""
        conds_names = self.df_all.condition.unique()
        num = 1
        for cond in conds_names:
            self.cond_dict[f'{cond}'] = num
            num+=1
        self.df_all = self.df_all.replace({"cond_int": self.cond_dict})
    
    def run(self):
        """ main pipeline """
        self.create_big_data()
        self.cond_names()
        self.df_all.to_csv(f"Data_Frame{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}.csv")

        
if __name__ == "__main__":
    pass
    # fix = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_fixations.csv')
    # event = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_messages.csv')
    # fix_obj = EyeFile(path=fix, fname=fix.name, id_num='01', design='1', data_type='fixations')
    # event_obj = EyeFile(path=event, fname=event.name, id_num='01', design='1', data_type='events')

    # data1 = IdData(fix_obj, event_obj)
    # data1.run()
    
    # fix2 = Path('CSV/FB/FB_integration_ID_02_design_2_time_04.11.18_13.32_fixations.csv')
    # event2 = Path('CSV/FB/FB_integration_ID_02_design_2_time_04.11.18_13.32_messages.csv')
    # fix_obj2 = EyeFile(path=fix2, fname=fix2.name, id_num='02', design='2', data_type='fixations')
    # event_obj2 = EyeFile(path=event2, fname=fix2.name, id_num='02', design='2', data_type='events')

    # data2 = IdData(fix_obj2, event_obj2)
    # data2.run()
  
    # big_data = AllId ([data1.df_id, data2.df_id])
    # big_data.run()
    # print (big_data.df_all)
   

    

