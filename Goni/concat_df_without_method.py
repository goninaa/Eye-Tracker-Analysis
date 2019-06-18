import pandas as pd
import numpy as np
import datetime

# create some mock data

data_eye = [(pd.Timestamp(1513393355, unit= 's'), pd.Timestamp(1513393463, unit= 's'), 90),
            (pd.Timestamp(1513393853, unit= 's'), pd.Timestamp(1513393900, unit= 's'), 80),
            (pd.Timestamp(1513394100, unit= 's'), pd.Timestamp(1513394500, unit ='s'), 150),
            (pd.Timestamp(1513394900, unit= 's'), pd.Timestamp(1513395300, unit= 's'), 85)]
df_eye = pd.DataFrame(data=data_eye, columns=['start', 'end', 'pixel'])

data_event = [(pd.Timestamp(1513393300, unit= 's'), pd.Timestamp(1513393450, unit= 's'), 'a'),
            (pd.Timestamp(1513393851, unit= 's'), pd.Timestamp(1513393876, unit= 's'), 'b'),
            (pd.Timestamp(1513393877, unit= 's'), pd.Timestamp(1513394177, unit= 's'), 'c'),
            (pd.Timestamp(1513394178, unit= 's'), pd.Timestamp(1513394580, unit= 's'), 'a')]
df_event = pd.DataFrame(data=data_event, columns=['start', 'end', 'event'])

# print (df_eye)
# print (df_event)

time_periods = pd.DataFrame({'time': pd.date_range(start = df_eye.start.min(), end = df_eye.end.max(), freq = 'S')}) #create all time-stamps
df_eye = time_periods.merge(df_eye, how='left', left_on='time', right_on='start').fillna(method='pad') #merge
# print (new_eye.iloc[70:150])
mask_eye = (df_eye['time'] > df_eye['start']) & (df_eye['time'] < df_eye['end'])
df_eye = df_eye.where(mask_eye)
df_eye = df_eye.dropna()
# print (fixed_eye.iloc[70:150])
df_eye.pop('start')
df_eye.pop('end')
df_eye.index = df_eye['time']
df_eye.pop('time')
# print (df_eye)


time_periods_event = pd.DataFrame({'time': pd.date_range(start = df_event.start.min(), end = df_event.end.max(), freq = 'S')}) #create all time-stamps
df_event = time_periods_event.merge(df_event, how='left', left_on='time', right_on='start').fillna(method='pad') #merge
mask_event = (df_event['time'] > df_event['start']) & (df_event['time'] < df_event['end'])
df_event = df_event.where(mask_event)
df_event = df_event.dropna()
df_event.pop('start')
df_event.pop('end')
df_event.index = df_event['time']
df_event.pop('time')
# print (df_event)

df_all = pd.concat ([df_event, df_eye], axis=1, sort = True)
df_all = df_all.dropna()

print (df_all.iloc[70:200])
