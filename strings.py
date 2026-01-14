import csv
from pandas import DataFrame
print('Strings')
with open('lang.csv',encoding='utf-8')as f:
    csv.register_dialect(t:=f.read(1), delimiter=t)
    f.seek(0)
    STRINGS = DataFrame(data = [row for row in csv.reader(f,t)]).replace(to_replace=None,value='',regex=[None])
    STRINGS.columns = STRINGS.iloc[0]
    STRINGS.set_index(STRINGS.columns[0], inplace=True)
            
