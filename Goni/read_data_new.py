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
    """ Pipeline to process twin Data instances  ,EyeFile"""
    # def __init__(self, fixations: fixations, events: events ):
    def __init__(self, fixations, events ):
        self.fixations = pd.read_csv(fixations.path)
        self.events = pd.read_csv(events.path)
        self.id_num = fixations.id_num
        self.design = fixations.design
        self.df_fixations = None

    def convert_fixations_to_df (self):
        """ convert fixations file to df with multi index"""
                                
        df = self.fixations
        df['ID'] = self.id_num
        df['design'] = self.design
        time_periods = pd.DataFrame({'time': pd.RangeIndex(start = df.startTime.min(), stop = df.endTime.max())}) #create all time-stamps
        df = time_periods.merge(df, how='left', left_on='time', right_on='startTime').fillna(method='pad') #merge
        mask = (df['time'] > df['startTime']) & (df['time'] < df['endTime'])
        df = df.where(mask)
        df = df.dropna()
        df.pop('startTime')
        df.pop('endTime')
        # df.drop(['startTime', 'endTime'], axis=1)
        self.df_fixations = df.set_index(['ID', 'design'])


    def concat_df (self):
        """ concat two df """
        # self.df_files = pd.concat ([df_event, df_eye], axis=1, sort = True)
        # self.df_files = self.df_files.dropna()
        
if __name__ == "__main__":

    fix = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_fixations.csv')
    event = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_messages.csv')
    fix_obj = EyeFile(path=fix, fname=fix.name, id_num='01', design='1', data_type='fixations')
    event_obj = EyeFile(path=event, fname=fix.name, id_num='01', design='1', data_type='events')

    data1 = ProcessData(fix_obj, event_obj)
    # print (data1.fixations)
    data1.convert_fixations_to_df()
    print (data1.df_fixations)



