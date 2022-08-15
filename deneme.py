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
data = []
dataTemp = []
dataRowPdf1 = []
dataRowPdf0 = []

def appendList(dataRow):
    data.append("62f3575ab51f8a773cde8ed1")
    data.append(datalistSPH[count])
    data.append(dataListUOM[count])
    data.append(dataListUOC[count])
    data.append(dataListPDF[count])
    dataTemp = data
    dataRow.append(dataTemp)

for i in dataListPDF:
    count += 1
    if (dataListPDF[count] == '1'):
        appendList(dataRowPdf1)
    else:
        appendList(dataRowPdf0)
    data = []



header = ['UserId', 'SPH', 'UOM', 'UOC',"PDF"]




with open('PdfUsageMemory.csv', 'w', encoding='UTF8',newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerows(dataRowPdf1)

with open('UsageOfServers.csv', 'w', encoding='UTF8',newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerows(dataRowPdf0)
