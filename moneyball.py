%matplotlib inline
import re
import pandas as pd
import matplotlib as plt
import numpy as np

master = pd.read_csv("data/Master.csv", sep=",")
batting = pd.read_csv("data/Batting.csv", sep=",")
salaries = pd.read_csv("data/Salaries.csv", sep=",")

master_list = pd.merge(batting, master)
master_list = pd.merge(master_list, salaries)

master_list.sort_values(by=['playerID', 'salary'])
master_list = master_list.groupby('playerID', group_keys=False).apply(lambda x: x.ix[x.salary.idxmax()]) master_list[["nameFirst", "nameLast", "finalGame", "H", "BB", "HBP", "AB", "SF", "salary"]]

""" Dates in 2015 seemed to be the final game for a lot of players and probably
    just denotes the end of the data collected. This gets any with a final game
    or a NaN value."""
date_time_finalGame = pd.to_datetime(master_list['finalGame'], format='%Y-%m-%d')
2015_and_NaN = master_list[(pd.to_datetime(master_list['finalGame'], format='%Y-%m-%d').dt.year == 2015) | master_list['finalGame'].isnull()]

""" Need to calculate OBP and sort by that and salary. """
