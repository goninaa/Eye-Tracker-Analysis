import attr
from attr.validators import instance_of
import pandas as pd
from pathlib import Path
import time
from process_GUI_input import *

class IdData:
    """Pipeline to process data of one ID on one design (both fixations and conditions).
    Attributes: fixations, events, id_num, design, df_fixations, df_cond, df_id.
    Methods: create_fixation_df, create_cond_df, merge_df, run count_data.
    """
    def __init__(self, fixations: EyeFile, events: EyeFile):
        self.fixations = pd.read_csv(fixations.path)
        self.events = pd.read_csv(events.path)
        self.id_num = fixations.id_num
        self.design = fixations.design
        self.df_fixations = pd.DataFrame()
        self.df_cond = pd.DataFrame()
        self.df_id = pd.DataFrame()

    def create_fixation_df(self) -> None:
        """Converts fixations file to data frame"""
        df = self.fixations.copy()
        df['ID'] = self.id_num
        df['design'] = self.design
        time_periods = pd.DataFrame({'time': pd.RangeIndex(start=df.startTime.min(), stop=df.endTime.max())}) #create all time-stamps
        df = time_periods.merge(df, how='left', left_on='time', right_on='startTime').fillna(method='pad') #merge
        mask = (df['time'] >= df['startTime']) & (df['time'] <= df['endTime'])
        df = df.where(mask).dropna().drop(['startTime', 'endTime'], axis=1)
        self.df_fixations = df

    def create_cond_df(self) -> None:
        """Creates conditions data frame"""
        df = self.events.copy()
        start = df.loc[df.loc[:, 'message'].str.contains('BLOCK_START'), :]
        end = df.loc[df.loc[:, 'message'].str.contains('STIM_DISP_END'), :]
        df = df.loc[~df.loc[:, 'message'].str.contains('BLOCK_END'), :]
        df['start'] = start.loc[:, 'time']
        df['end'] = end.loc[:, 'time']
        df['condition'] = df.loc[:, 'message'].str.split(':').str[2].str.strip()
        df = df.fillna(method='pad')
        df = df.rename(index=str, columns={"time": "original_time"})
        time_periods = pd.DataFrame({'time': pd.RangeIndex(start=df.start.min(), stop=df.end.max())})
        df = time_periods.merge(df, how='left', left_on='time', right_on='start').fillna(method='pad') 
        mask = (df['time'] >= df['start']) & (df['time'] <= df['end'])
        df = df.where(mask).dropna().drop(['original_time', 'start', 'end', 'message'], axis=1)
        df['cond_int'] = df['condition']
        self.df_cond = df

    def merge_df(self) -> None:
        """Merges conditions and fixations dataframes into one multi-index (ID, design) data frame"""
        df = self.df_fixations.merge(self.df_cond, on='time')
        df = df.dropna()
        self.df_id = df.set_index(['ID', 'design'])

    def count_df(self) -> None:
        """Optional function. Does not call by func run(). Incompatible with func merge_df().
        Merges conditions and fixations dataframes into one multi-index data frame, 
        with the count of time as data, and ID, design and condition as multi-index
        """
        df = self.df_fixations.merge(self.df_cond, on='time')
        df = df.dropna()
        df = df.groupby(['condition', 'aveH', 'aveV']).count()
        self.df_id = df.reset_index().set_index(['ID', 'design', 'condition'])
    
    def run(self) -> None:
        """Main pipeline"""
        self.create_fixation_df()
        self.create_cond_df()
        self.merge_df()
    
@attr.s
class AllId:
    """A unified dataframe, multi-indexed by ID and design.
    Attributes: df_list, df_all, cond_dict.
    Methods: merge_df, create_big_data, cond_names, save_csv, run.
    """
    df_list = attr.ib(validator=instance_of(list))
    df_all = attr.ib(default=pd.DataFrame)
    cond_dict = attr.ib(default=attr.Factory(dict))

    def merge_df(self, basic_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
        """Appends dataframe given by create_big)data func into one multi-index data frame"""
        df_merge = pd.concat([basic_df, df])
        df_merge = df_merge.dropna()
        return df_merge

    def create_big_data(self) -> None:
        """Merges all data frames in the list into one big data frame"""
        basic_df = self.df_list.pop(0)
        for df in self.df_list:
            basic_df = self.merge_df(basic_df, df)
        self.df_all = basic_df

    def cond_names(self) -> None:
        """Replaces all conditions names in 'cond_int' column into int"""
        conds_names = self.df_all.condition.unique()
        num = 1
        for cond in conds_names:
            self.cond_dict[f'{cond}'] = num
            num+=1
        self.df_all = self.df_all.replace({"cond_int": self.cond_dict})

    def save_csv(self) -> None:
        """Saves dataframe into csv file"""
        output_file = (f"Data_Frame_{pd.Timestamp.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv")
        output_dir = Path('Results')
        output_dir.mkdir(parents=True, exist_ok=True)
        self.df_all.to_csv(output_dir / output_file)

    def run(self) -> None:
        """Main pipeline"""
        self.create_big_data()
        self.cond_names()
        self.save_csv()

        
if __name__ == "__main__":
    pass
    