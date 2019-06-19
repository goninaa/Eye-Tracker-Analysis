import pandas as pd
import attr
from attr.validators import instance_of
from mock_EyeFile_pair import *

# @attr.s
# class ProcessData:
#     fixations = attr.ib(validator=instance_of(EyeFile)) 
#     events = attr.ib(validator=instance_of(EyeFile)) 
        
#     def read_file (self):
#         pd.read_csv(fname)

class ProcessData:
    """ Pipeline to process data of one ID on one design
    (both fixations and conditions)"""
    # def __init__(self, fixations: fixations, events: events ):
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
        # df = df.set_index(['ID', 'design'])
        self.df_fixations = df
        # df.drop(['startTime', 'endTime'], axis=1)
        # self.df_fixations = df.set_index(['ID', 'design'])

    def create_cond_df (self):
        """ create conditions data frame """
        df = self.events.copy()
        start = df.loc[df.loc[:, 'message'].str.contains('BLOCK_START'), :]
        end = df.loc[df.loc[:, 'message'].str.contains('STIM_DISP_END'), :]
        df = df.loc[~df.loc[:, 'message'].str.contains('BLOCK_END'), :]
        df['start'] = start.loc[:, 'time']
        df['end'] = end.loc[:, 'time']
        df['condition'] = df.loc[:, 'message'].str.split(':').str[2]
        df = df.fillna(method= 'pad')
        df = df.rename(index=str, columns={"time": "orignal_time"})
        # df['ID'] = self.id_num
        # df['design'] = self.design

        time_periods = pd.DataFrame({'time': pd.RangeIndex(start = df.start.min(), stop = df.end.max())})
        df = time_periods.merge(df, how='left', left_on='time', right_on='start').fillna(method='pad') #merge
        mask = (df['time'] >= df['start']) & (df['time'] <= df['end'])
        df = df.where(mask)
        df = df.dropna()
        df.pop('orignal_time')
        df.pop('start')
        df.pop('end')
        df.pop('message')
        # df = df.set_index(['ID', 'design'])
        self.df_cond = df


    def merge_df (self):
        """ merge conditions and fixations dataframes into one multi-index
        data frame, with ID and design """
        # df = pd.concat ([self.df_fixations, self.df_events], axis=1, sort = True)
        # df = pd.concat ([self.df_fixations, self.df_events], axis = 1)
        df = self.df_fixations.merge(self.df_cond, on = 'time')
        # df = df.dropna()
        self.df_id = df
        self.df_id = df.set_index(['ID', 'design'])

    class IdData:
        """ data frame of all repetitions of one ID """
        pass
        
        
if __name__ == "__main__":

    fix = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_fixations.csv')
    event = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_messages.csv')
    fix_obj = EyeFile(path=fix, fname=fix.name, id_num='01', design='1', data_type='fixations')
    event_obj = EyeFile(path=event, fname=fix.name, id_num='01', design='1', data_type='events')

    data1 = ProcessData(fix_obj, event_obj)
    # print (data1.fixations)
    data1.create_fixation_df()
    # print (data1.df_fixations)

    # print (data1.events)
    data1.create_cond_df()
    # print (data1.df_events)
    data1.merge_df()
    print (data1.df_id)



