#
# budget-discover.py : A budget tool for tracking income and expenses. Requires a .csv file of transactions from Chase Bank and Discover.
#

import pandas as pd
import os
from datetime import date

# clear screen on any operating system

from platform   import system as system_name
from subprocess import call   as system_call

command = 'cls' if system_name().lower().startswith('win') else 'clear'
system_call([command])

# read correct files
# remove given headers then add custom ones

file_c = input('\n''Enter the Chase Bank .csv file path''\n\n')
basename = os.path.splitext(os.path.basename(file_c))[0]
df_c1 = pd.read_csv(file_c, names=['details','date','description','amount','type','balance','check or slip #','dropme'], skiprows=1, delimiter=',')

file_d = input('\n''Enter the Discover .csv file path''\n\n')
df_d1 = pd.read_csv(file_d, names=['transaction date','posted date','description','amount','category'], skiprows=1, delimiter=',')

df_d1 = df_d1.drop(columns=['transaction date'])
df_d1 = df_d1.drop(columns=['category'])

# remove unnecessary columns

df_c1 = df_c1.drop(columns=['details'])
df_c1 = df_c1.drop(columns=['type'])
df_c1 = df_c1.drop(columns=['balance'])
df_c1 = df_c1.drop(columns=['check or slip #'])
df_c1 = df_c1.drop(columns=['dropme'])

# remove discover transactions from other months

df_c1['date'] = pd.to_datetime(df_c1['date'])
df_c1 = df_c1.sort_values(by='date', ascending=False)
df_d1['posted date'] = pd.to_datetime(df_d1['posted date'])
df_d1 = df_d1.sort_values(by='posted date', ascending=False)
df_month = df_c1['date'].dt.month
month = df_month[0]
df_year = df_c1['date'].dt.year
year = df_year[0]
if month == 1:
    month_start = 11
    month_end = 12
    year_start = year - 1
    year_end = year - 1
    start = date(year_start,month_start,21)
    end = date(year_end,month_end,20)
if month == 2:
    month_start = 12
    month_end = month - 1
    year_start = year - 1
    year_end = year
    start = date(year_start,month_start,21)
    end = date(year_end,month_end,20)
if 2 < month < 13:
    month_start = month - 2
    month_end = month - 1
    year_start = year
    year_end = year
    start = date(year_start,month_start,21)
    end = date(year_end,month_end,20)
df_d1 = df_d1[(df_d1['posted date'] > f'{start}') & (df_d1['posted date'] < f'{end}')]

# cash flow check

df_c_total = df_c1.drop(columns=['date']).drop(columns=['description']).abs().sum().round(2)
c_total = df_c_total['amount']

i_c = 0
i_d = 0
category =[]
amount = []

# print rows 1 by 1
# ask for budget category for each transaction
# store budget category and associated amount

def selectFromDict(options, name):
    index = 0
    default = 0
    indexValidList = []
    print('Select a ' + name + ':')
    for optionName in options:
        index = index + 1
        indexValidList.extend([options[optionName]])
        print(str(index) + ') ' + optionName)
    inputValid = False
    while not inputValid:
        inputRaw = int(input(name + ': ') or default)
        inputNo = int(inputRaw) - 1
        if inputNo > -1 and inputNo < len(indexValidList):
            selected = indexValidList[inputNo]
            print('Selected ' +  name + ': ' + selected)
            inputValid = True
            break
        else:
            print('Please select a valid ' + name + ' number')
    return selected

# current categories

df_0 = pd.read_csv('categories.csv')
categories = df_0['category'].tolist()

options = {category: category for category in categories}

option = []
system_call([command])

for index, row in df_c1.iterrows():
    print("Chase ", df_c1.iloc[[i_c]].to_string(header=None, index=False),"\n")
    option.append(selectFromDict(options, 'option'))
    amount.append(df_c1.iloc[i_c,2])
    system_call([command])
    i_c = i_c + 1

for index, row in df_d1.iterrows():
    print("Discover ", df_d1.iloc[[i_d]].to_string(header=None, index=False),"\n")
    option.append(selectFromDict(options, 'option'))
    amount.append(df_d1.iloc[i_d,2])
    system_call([command])
    i_d = i_d + 1

# write new .csv file with all information from previous steps

modified = {'category': option, 'amount': amount}
idx_cd = pd.Index(range(0,i_c+i_d,1))
df_cd2 = pd.DataFrame(modified, index=idx_cd)
df_cd2 = df_cd2[df_cd2["category"].str.contains("Discover") == False]
df_cd2 = df_cd2.to_csv("intermediate.csv", index=False, sep= ',', encoding='utf-8')

# read the new .csv file
# sort by alphabetical order
# send income to top
# send expenses to bottom, then sum repeat categories

df_cd3 = pd.read_csv('intermediate.csv')
df_cd3 = df_cd3.sort_values("category")
df_cd4 = df_cd3['amount'] > 0

# send income to top
# add rest of categories that do not have an amount
# sum repeat categories

df_cd5 = df_cd3[df_cd4].copy()
df_cd5 = df_cd5.groupby(['category'], as_index=False)['amount'].sum()
df_cd6 = pd.read_csv('categories.csv')
df_cd7 = pd.concat([df_cd5,df_cd6], ignore_index=True)
df_cd7 = df_cd7.sort_values(by=['category', 'amount'])

# send expenses to bottom
# add rest of categories that do not have an amount
# sum repeat categories

df_cd8 = df_cd3[~df_cd4].copy()
df_cd8['amount'] *= -1
df_cd8 = df_cd8.groupby(['category'], as_index=False)['amount'].sum()
df_cd8 = pd.concat([df_cd7, df_cd8], ignore_index=True)
df_cd8 = df_cd8.sort_values(by=['category', 'amount'])

# combine dataframes

df_cd9 = df_cd8.groupby('category')['amount'].sum().reset_index()
df_cd9['category'] = pd.Categorical(df_cd9['category'], categories=categories, ordered=True)
df_cd9 = df_cd9.sort_values('category')

# cash flow check

df_cd_total = df_cd9.drop(columns=['category']).abs().sum().round(2)
cd_total = df_cd_total['amount']

if not c_total == cd_total:
    print('Error: totals do not match before and after.''\n',c_total,'\n',cd_total,'\n')

# write to final .csv file destination

df_cd10 = df_cd9.to_csv(f"output-{basename}.csv", index=False, sep= ',', encoding='utf-8')