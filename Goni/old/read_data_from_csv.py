import pandas as pd
# from collections import defaultdict


class Data:
    """ data frame of one ID on one repetition (both eyes and events)"""
    def __init__ (self, fname_eyes, fname_events):
        #assume gui checked the files refer to the same id and rep
        self._fname_eyes = fname_eyes
        self._fname_events = fname_events
        self._df_eyes = pd.read_csv(self._fname_eyes)
        self._df_events = pd.read_csv(self._fname_events)
        self.df_files = pd.DataFrame()
        self.metadata = {'id':fname_eyes[4:8], 'rep': fname_eyes[8:10]} #change slicing

class ProcessData:
    """ """

    def convert_to_df (self):
        """ convert file to readeble df"""
        pass

    def concat_df (self):
        """ concat two df """
        # self.df_files = pd.concat ([df_event, df_eye], axis=1, sort = True)
        # self.df_files = self.df_files.dropna()

        
class IdData:
    """ data frame of all repetitions of one ID """
    pass

class BigData:
    """ data frame of all IDs repetitions """
    pass


if __name__ == "__main__":

    fname1 = 'test_17-06-18.csv'
    fname2 = 'test_17-06-18.csv'

    data1 = Data(fname1, fname2)
    print (data1.data.head())

    # fname = 'test_17-06-18.csv'
    # data = pd.read_csv(fname)
    # print (data)
