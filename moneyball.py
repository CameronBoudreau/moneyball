%matplotlib inline
import re
import pandas as pd
import matplotlib as plt
import numpy as np

master = pd.read_csv("data/Master.csv", sep=",")
master = master[["playerID", "nameFirst", "nameLast", "finalGame"]]

batting = pd.read_csv("data/Batting.csv", sep=",")
batting = batting[["playerID", "H", "BB", "HBP", "AB", "SF"]]
mean_batting = batting.sort_values('playerID').groupby('playerID').mean()
mean_batting.fillna(value=0)
mean_batting.reset_index(level=0, inplace=True)

salaries = pd.read_csv("data/Salaries.csv", sep=",")
salaries = salaries[["playerID", "yearID", 'salary']]
salaries = salaries.sort_values(['playerID', 'yearID']).drop_duplicates('playerID', keep='last')
salaries = salaries[['playerID', 'salary']]

fielding = pd.read_csv("data/FieldingPost.csv", sep=",")
fielding = fielding.sort_values(['playerID', 'yearID'])
fielding = fielding.drop_duplicates('playerID', keep='last')
fielding = fielding[['playerID', 'POS']].copy()
fielding.sort_values('playerID')

master_list = master.merge(mean_batting)
master_list = pd.merge(master_list, salaries)
master_list = pd.merge(master_list, fielding)

only_2015 = master_list[(pd.to_datetime(master_list['finalGame'], format='%Y-%m-%d').dt.year == 2015) | master_list['finalGame'].isnull()].copy()

def get_obp(H, AB, BB, SF, HBP=0):
    return ((H+BB+HBP)/(AB+BB+HBP+SF))

only_2015['OBP'] = get_obp(only_2015['H'], only_2015['AB'], only_2015['BB'], only_2015['SF'], only_2015['HBP'])

clean_2015 = only_2015[(only_2015.OBP != 0) & (only_2015.OBP != 1) & (only_2015.OBP != None) & (only_2015.OBP.notnull())]

final_list = clean_2015[['POS', 'OBP', 'salary', 'playerID', 'nameFirst', 'nameLast']].copy()
final_list = final_list.sort_values(['POS', 'OBP'], ascending=False)
final_list.groupby('POS')

final_list = final_list[(final_list.OBP >= 0.36)]
final_list.sort_values(['POS', 'salary'], ascending=False)

final_list.sort_values(['POS', 'salary'], ascending=False).drop_duplicates('POS', keep='last')
