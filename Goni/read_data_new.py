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

class IdData:
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
        df = self.df_fixations.merge(self.df_cond, on = 'time')
        df = df.dropna()
        self.df_id = df
        self.df_id = df.set_index(['ID', 'design'])

    def run (self):
        """ main pipeline """
        self.create_fixation_df()
        self.create_cond_df()
        self.merge_df()


    # class IdData:
    #     """ data frame of all designs of one ID 
    #     (from several ProcessData) """
    #     def __init__(self, df1, df2):
    #         self.id_num = fixations.id_num
    #         self.design = fixations.design
    #         self.df_fixations = None
    #         self.df_cond = None
    #         self.df_id = None

    #         self.designs = ()
    #         self.df_all_designs = None

    #     def merge_df (self):
    #         """ merge two ProcessData.merge_df of same ID into one multi-index
    #         data frame """

    #         df = self.df2.merge(self.df_cond, on = 'time')
    #         # df = df.dropna()
    #         # self.df_id = df.set_index(['ID', 'design'])
    #         self.df_all_designs = df
    
class AllId:
    """ data frame of all IDs repetitions.
    from several IdData """
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2
        self.df_all = None

    def merge_df (self):
        """ merge IdData.merge_df into one multi-index
        data frame """
        df_all = pd.concat ([self.df1, self.df2])
        # df = self.df1.merge(self.df2)
        # df = df.dropna()
        # self.df_id = df.set_index(['ID', 'design'])
        self.df_all = df_all
        
if __name__ == "__main__":

    fix = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_fixations.csv')
    event = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_messages.csv')
    fix_obj = EyeFile(path=fix, fname=fix.name, id_num='01', design='1', data_type='fixations')
    event_obj = EyeFile(path=event, fname=event.name, id_num='01', design='1', data_type='events')

    data1 = IdData(fix_obj, event_obj)
    data1.run()
    # print (data1.df_id)

    fix2 = Path('CSV/FB/FB_integration_ID_02_design_2_time_04.11.18_13.32_fixations.csv')
    event2 = Path('CSV/FB/FB_integration_ID_02_design_2_time_04.11.18_13.32_messages.csv')
    fix_obj2 = EyeFile(path=fix2, fname=fix2.name, id_num='02', design='2', data_type='fixations')
    event_obj2 = EyeFile(path=event2, fname=fix2.name, id_num='02', design='2', data_type='events')

    data2 = IdData(fix_obj2, event_obj2)
    data2.run()
  # print (data1.fixations)
    # data1.create_fixation_df()
    # # print (data1.df_fixations)
    # # print (data1.events)
    # data1.create_cond_df()
    # # print (data1.df_events)
    # data1.merge_df()
    # print (data2.df_id)
    big_data = AllId (data1.df_id, data2.df_id)
    big_data.merge_df()
    print (big_data.df_all)

