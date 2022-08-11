from itertools import zip_longest
import  random
import csv
import time
from datetime import datetime
import json
import bson




datalistSPH = []
dataListUOM = []
dataListUOC = []
dataListPDF = []
dataListWSPH = []
dataListWUOM = []
dataListWUOC = []





dataListUser = []
user ="62f3575ab51f8a773cde8ed1"


for i in range(100):
    SPH = round(random.randint(50, 200))
    PDF = 1
    dataListUser.append(user)
    dataListPDF.append(PDF)
    if(SPH>50 and SPH <= 100):
        UOM = round(random.uniform(0,25),1)
        UOC = round(random.uniform(0,25),1)
        datalistSPH.append(SPH)
        dataListUOM.append(UOM)
        dataListUOC.append(UOC)
    elif(SPH>100 and SPH<=150):
        UOM = round(random.uniform(25, 50), 1)
        UOC = round(random.uniform(25, 50), 1)
        datalistSPH.append(SPH)
        dataListUOM.append(UOM)
        dataListUOC.append(UOC)
    elif(SPH>150 and SPH<=200):
        UOM = round(random.uniform(50, 75), 1)
        UOC = round(random.uniform(50, 75), 1)
        datalistSPH.append(SPH)
        dataListUOM.append(UOM)
        dataListUOC.append(UOC)
    elif (SPH > 200 and SPH <= 250):
        UOM = round(random.uniform(75, 100), 1)
        UOC = round(random.uniform(75, 100), 1)
        datalistSPH.append(SPH)
        dataListUOM.append(UOM)
        dataListUOC.append(UOC)
    else:
        UOM = round(random.uniform(75, 100), 1)
        UOC = round(random.uniform(75, 100), 1)
        datalistSPH.append(SPH)
        dataListUOM.append(UOM)
        dataListUOC.append(UOC)






"""for i in range(100):
    WSPH = round(random.randint(200,500))
    
    if(WSPH>200 and WSPH <= 250):
        WUOM = round(random.uniform(0,25),1)
        WUOC = round(random.uniform(0,25),1)
        dataListWSPH.append(WSPH)
        dataListUOM.append(WUOM)
        dataListWUOC.append(WUOC)
    elif(WSPH>250 and WSPH<=300):
        WUOM = round(random.uniform(25,50),1)
        WUOC = round(random.uniform(25,50),1)
        dataListWSPH.append(WSPH)
        dataListWUOM.append(WUOM)
        dataListWUOC.append(WUOC)
    elif(WSPH>300 and WSPH<=350):
        WUOM = round(random.uniform(50, 75), 1)
        WUOC = round(random.uniform(50, 75), 1)
        dataListWSPH.append(WSPH)
        dataListWUOM.append(WUOM)
        dataListWUOC.append(WUOC)
    elif (WSPH > 350 and WSPH <= 400):
        WUOM = round(random.uniform(75, 100), 1)
        WUOC = round(random.uniform(75, 100), 1)
        dataListWSPH.append(WSPH)
        dataListWUOM.append(WUOM)
        dataListWUOC.append(WUOC)
    else:
        WUOM = round(random.uniform(75, 100), 1)
        WUOC = round(random.uniform(75, 100), 1)
        dataListWSPH.append(WSPH)
        dataListWUOM.append(WUOM)
        dataListWUOC.append(WUOC)"""



# dakikada kaç submission aldığı
# kullandığı memory
# kullandığı cpu
# almak istediği submission
# ne kadar memory
# ne kadar cpu



d = [dataListUser,datalistSPH, dataListUOM,dataListUOC,dataListPDF]
export_data = zip_longest(*d, fillvalue = '')
with open('PdfUsageMemory.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("UserId","SPH", "UOM","UOC", "PDF"))
      wr.writerows(export_data)
myfile.close()



"""
d2 = [dataListUser,dataListWSPH, dataListWUOM,dataListWUOC]
export_data2 = zip_longest(*d2, fillvalue = '')
with open('WantOfServers.csv', 'w', encoding="ISO-8859-1", newline='') as myfile2:
    wr2 = csv.writer(myfile2)
    wr2.writerow(("UserId","WSPH", "WUOM", "WUOC"))
    wr2.writerows(export_data2)
myfile2.close()
"""
