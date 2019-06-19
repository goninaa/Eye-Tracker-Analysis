import pandas as pd
import attr
from attr.validators import instance_of

# @attr.s
# class ProcessData:
#     fixations = attr.ib(validator=instance_of(EyeFile)) 
#     events = attr.ib(validator=instance_of(EyeFile)) 
        
#     def read_file (self):
#         pd.read_csv(fname)

class ProcessData:
    """ Pipeline to process twin Data instances  ,EyeFile"""
    def __init__(self, fixations: fixations, events: events ):
        self.fixations = pd.read_csv(fixations.path)
        self.events = pd.read_csv(events.path)
        # self.result = {}
        # self.metadata = datacont.metadata

    def convert_fixations_to_df (self):
    """ convert file to readeble df"""
    df = self.fixations
    time_periods = pd.DataFrame({'time': pd.date_range(start = df.start.min(), end = df.end.max(), freq = 'S')}) #create all time-stamps
    df = time_periods.merge(df, how='left', left_on='time', right_on='start').fillna(method='pad') #merge
    # print (new_eye.iloc[70:150])
    mask_eye = (df['time'] > df['start']) & (df['time'] < df['end'])
    df = df.where(mask_eye)
    df = df.dropna()
    # print (fixed_eye.iloc[70:150])
    df.pop('start')
    df.pop('end')
    df.index = df_eye['time']
    df.pop('time')
    # print (df_eye)
    pass

    def concat_df (self):
        """ concat two df """
        # self.df_files = pd.concat ([df_event, df_eye], axis=1, sort = True)
        # self.df_files = self.df_files.dropna()
        
    # exmple:
    # def process(self):
    #     """ Mock processing pipeline """
    #     self.result['sum'] = self.datacont.sum()
    #     means = [x.mean() for x in self.datacont.data]
    #     self.result['mean'] = means
    #     return self.result
