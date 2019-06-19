import pandas as pd
import numpy as np

id_num = ['345']*15
design = ['1'] *15
indexes = list(zip(*[id_num,design]))

times = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
con = ['a','a','b','a','b','b','b','a','a','b','a','b','a','a','a']
aveH = [2,4,2,6,10,15,14,3,7,8,10,15,10,10,10]
aveV = [5,10,5,6,5,15,1,3,12,10,5,15,5,5,5]
data = np.array([times,con,aveH, aveV]).T

index = pd.MultiIndex.from_tuples(indexes,names = ['ID','design'])
#index = pd.MultiIndex.from_product([[id_num], [design]],
                                #    names=['ID', 'design']) 
columns = pd.MultiIndex.from_product([['time', 'condition', 'aveH', 'aveV']],
                                    names = [None])

example_data = pd.DataFrame(data, index=index, columns=columns)

print (example_data)

