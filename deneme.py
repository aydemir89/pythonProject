import csv
from itertools import zip_longest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import json
import rabbitmqReceiver
import time

file = csv.DictReader(open('dataSet.csv','r'))
datalistSPH = []
dataListUOM = []
dataListUOC = []
dataListPDF = []
dataListPDF2 = []
dataListUser = []
temp = []
user ="62f3575ab51f8a773cde8ed1"
for col in file:
    datalistSPH.append(col['SPH'])
    dataListUOM.append(col['UOM'])
    dataListUOC.append(col['UOC'])
    dataListPDF.append(col['PDF'])
count =-1
flag = 0

def delete():
    del dataListPDF[:]

len=len(dataListPDF)

while 1:
    if flag == 0:
        if (dataListPDF[count] == '1'):
            while 1:
                if flag == 0:
                    delete()
                    flag = 1
                    break
            dataListPDF.append(1)
            print(dataListPDF)
            count += 1





