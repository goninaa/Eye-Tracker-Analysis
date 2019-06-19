import pandas as pd

id_num = '345'
rep = '1'
data = ()

index = pd.MultiIndex.from_product([[id_num], [rep]],
                                   names=['ID', 'design']) 
columns = pd.MultiIndex.from_product([['time', 'condition', 'aveH', 'aveV']],
                                    names = [None])

example_data = pd.DataFrame(data, index=index, columns=columns)

print (example_data)

