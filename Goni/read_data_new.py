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
        self.id_num = fixations.id_num
        self.design = fixations.design

    def convert_fixations_to_df (self):
    """ convert file to readeble df"""
    index = pd.MultiIndex.from_product([[self.id_num], [self.design]],
                                    names=['ID', 'design']) 
    df = self.fixations
    time_periods = pd.DataFrame({'time': pd.date_range(start = df.startTime.min(), end = df.endTime.max(), freq = 'S')}) #create all time-stamps
    df = time_periods.merge(df, how='left', left_on='time', right_on='start').fillna(method='pad') #merge
    mask = (df['time'] > df['start']) & (df['time'] < df['end'])
    df = df.where(mask)
    df = df.dropna()
    df.drop(['start', 'end'], axis=1
    
    

    def concat_df (self):
        """ concat two df """
        # self.df_files = pd.concat ([df_event, df_eye], axis=1, sort = True)
        # self.df_files = self.df_files.dropna()
        

    id_num = '345'
    design = '1'
    data = ()

    index = pd.MultiIndex.from_product([[id_num], [design]],
                                    names=['ID', 'design']) 
    columns = pd.MultiIndex.from_product([['time', 'condition', 'aveH', 'aveV']],
                                        names = [None])

    example_data = pd.DataFrame(data, index=index, columns=columns)
    # exmple:
    # def process(self):
    #     """ Mock processing pipeline """
    #     self.result['sum'] = self.datacont.sum()
    #     means = [x.mean() for x in self.datacont.data]
    #     self.result['mean'] = means
    #     return self.result
