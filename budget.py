#
# budget.py : A budget tool for tracking income and expenses. Requires a .csv file of transactions from Chase bank.
#

import pandas as pd
import os

# clear screen

from platform   import system as system_name
from subprocess import call   as system_call

command = 'cls' if system_name().lower().startswith('win') else 'clear'
system_call([command])

# read correct file
# remove given headers then add custom ones

date = input('Enter the .csv file path''\n')
file = f'{date}.CSV'
basename = os.path.splitext(os.path.basename(file))[0]
df1 = pd.read_csv(file, names=['details','date','description','amount','type','balance','check or slip #','dropme'], skiprows=1, delimiter=',')

# remove unnecessary columns

df1 = df1.drop(columns=['details'])
df1 = df1.drop(columns=['type'])
df1 = df1.drop(columns=['balance'])
df1 = df1.drop(columns=['check or slip #'])
df1 = df1.drop(columns=['dropme'])

# sum total cash flow
df_total_before = df1.drop(columns=['date']).drop(columns=['description']).abs().sum()

i = 0
category =[]
amount = []

# print rows 1 by 1
# ask for budget category for each transaction
# store budget category and associated amount

def selectFromDict(options, name):

    index = 0
    indexValidList = []
    print('Select a ' + name + ':')
    for optionName in options:
        index = index + 1
        indexValidList.extend([options[optionName]])
        print(str(index) + ') ' + optionName)
    inputValid = False
    while not inputValid:
        inputRaw = input(name + ': ')
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

df0 = pd.read_csv('categories.csv')
categories = df0['category'].tolist()

options = {category: category for category in categories}

option = []
system_call([command])

for index, row in df1.iterrows():
    print(df1.iloc[[i]].to_string(header=None, index=False),"\n")
    option.append(selectFromDict(options, 'option'))
    amount.append(df1.iloc[i,2])
    system_call([command])
    i = i + 1

# write new .csv file with all information from previous steps

modified = {'category': option, 'amount': amount}
idx = pd.Index(range(0,i,1))
df2 = pd.DataFrame(modified, index=idx)
df2 = df2.to_csv("intermediate.csv", index=False, sep= ',', encoding='utf-8')

# read the new .csv file
# sort by alphabetical order
# send income to top
# send expenses to bottom, then sum repeat categories

df3 = pd.read_csv('intermediate.csv')
df3 = df3.sort_values("category")
df4 = df3['amount'] > 0

# send income to top
# add rest of categories that do not have an amount
# sum repeat categories

df5 = df3[df4].copy()
df5 = df5.groupby(['category'], as_index=False)['amount'].sum()
df6 = pd.read_csv('categories.csv')
df7 = pd.concat([df5,df6], ignore_index=True)
df7 = df7.sort_values(by=['category', 'amount'])

# send expenses to bottom
# add rest of categories that do not have an amount
# sum repeat categories

df8 = df3[~df4].copy()
df8['amount'] *= -1
df8 = df8.groupby(['category'], as_index=False)['amount'].sum()
df8 = pd.concat([df7, df8], ignore_index=True)
df8 = df8.sort_values(by=['category', 'amount'])

# combine dataframes

df9 = df8.groupby('category')['amount'].sum().reset_index()
df9['category'] = pd.Categorical(df9['category'], categories=categories, ordered=True)
df9 = df9.sort_values('category')

# write to final .csv file destination

df10 = df9.to_csv(f"output-{basename}.csv", index=False, sep= ',', encoding='utf-8')