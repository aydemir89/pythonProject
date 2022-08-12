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


rabbitmqReceiver.main()
lastValue = 0
pdfValue = 0


def main_(SPH,IsPdfSend):
    print("IsPdfSend = " ,IsPdfSend)
    # Data Collection & Analysis

    regressor = LinearRegression()
    #PdfUsageMemory kullandığı kısım



    if( IsPdfSend == 0 ):
        insurance_dataset = pd.read_csv('UsageOfServers.csv')

        # UsageOfServers.csv kullandığı#



        # first 5 rows of the dataframe
        insurance_dataset.head()
        # number of rows and columns
        insurance_dataset.shape
        insurance_dataset.info()

        # checking for missing values
        insurance_dataset.isnull().sum()
        # statistical measures
        insurance_dataset.describe()
        # print(insurance_dataset.describe())

        insurance_dataset.plot.scatter(x='SPH', y='UOC', title='asasasas')
        # splitting feature and target

        # X=insurance_dataset.drop(columns='scores', axis = 1)
        # Y=insurance_dataset['scores']
        X = insurance_dataset['SPH'].values.reshape(-1, 1)
        Y = insurance_dataset['UOC'].values.reshape(-1, 1)
        Z = insurance_dataset['UOM'].values.reshape(-1, 1)

        # Splitting the data into training data and testing data
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        # print(X.shape,X_train.shape,X_test.shape)

        # Model Training
        # Linear Regression

        regressor.fit(X_train, Y_train)
        print(regressor.intercept_)
        # Model Evaluation
        print(regressor.coef_)

        # prediction on training data
        training_data_prediction = regressor.predict(X_train)
        # R squared value
        r2_train = metrics.r2_score(Y_train, training_data_prediction)
        print('R square value:', r2_train)

        test_data_prediction = regressor.predict(X_test)
        r2_test = metrics.r2_score(Y_test, test_data_prediction)
        print('R square value:', r2_test)

        input_data_as_numpy_array = np.asarray(SPH)
        input_data_reshaped = input_data_as_numpy_array.reshape(-1, 1)
        prediction = regressor.predict(input_data_reshaped)
        print("UOC")
        print(prediction[0])

        """-----------------------------------------------------"""
        insurance_dataset.plot.scatter(x='SPH', y='UOM', title='asasasas')
        # Splitting the data into training data and testing data
        X_train, X_test, Z_train, Z_test = train_test_split(X, Z, test_size=0.2, random_state=42)
        # Model Training
        # Linear Regression
        regressor.fit(X_train, Z_train)
        # prediction on training data
        training_data_prediction1 = regressor.predict(X_train)
        # R squared value
        r2_train1 = metrics.r2_score(Z_train, training_data_prediction1)
        test_data_prediction1 = regressor.predict(X_test)
        r2_test1 = metrics.r2_score(Z_test, test_data_prediction1)

        input_data_as_numpy_array1 = np.asarray(SPH)
        input_data_reshaped1 = input_data_as_numpy_array1.reshape(-1, 1)
        prediction1 = regressor.predict(input_data_reshaped1)
        print("UOM")
        print(prediction1[0])

        dictionary = {
            "id": "62f3575ab51f8a773cde8ed1",
            "SPH": SPH,
            "UOM": prediction1[0][0],
            "UOC": prediction[0][0],
            "IsPdfSend": 0
        }
        out_file = open("data.json", "w")
        json_object = json.dump(dictionary, out_file, indent=6)
        out_file.close()

        plt.figure(figsize=(10, 10))
        sns.countplot(x='SPH', data=insurance_dataset)
        plt.title('Submission per hour Distribution')
        plt.show()

        plt.figure(figsize=(10, 10))
        sns.distplot(insurance_dataset['UOM'])
        plt.title('Usage of memory')
        plt.show()

        plt.figure(figsize=(10, 10))
        sns.countplot(x='UOC', data=insurance_dataset)
        plt.title('Usage of cpu')
        plt.show()


    elif(IsPdfSend == 1):

        pdf_dataset = pd.read_csv('PdfUsageMemory.csv')
        pdf_dataset.head()
        pdf_dataset.shape
        pdf_dataset.info()
        pdf_dataset.isnull().sum()
        pdf_dataset.describe()

        pdf_dataset.plot.scatter(x='SPH', y='UOC', title='asasasas')
        Xp = pdf_dataset['SPH'].values.reshape(-1, 1)
        Yp = pdf_dataset['UOC'].values.reshape(-1, 1)
        Zp = pdf_dataset['UOM'].values.reshape(-1, 1)

        Xp_train, Xp_test, Yp_train, Yp_test = train_test_split(Xp, Yp, test_size=0.2, random_state=42)
        regressor.fit(Xp_train, Yp_train)

        training_data_prediction_pdf = regressor.predict(Xp_train)
        r2p_train = metrics.r2_score(Yp_train, training_data_prediction_pdf)

        test_data_prediction_pdf = regressor.predict(Xp_test)
        r2p_test = metrics.r2_score(Yp_test, test_data_prediction_pdf)
        print('R square value:', r2p_test)

        input_data_as_numpy_array_pdf = np.asarray(SPH)
        input_data_reshaped_pdf = input_data_as_numpy_array_pdf.reshape(-1, 1)
        prediction_pdf = regressor.predict(input_data_reshaped_pdf)
        print("UOC")
        print(prediction_pdf[0])

        pdf_dataset.plot.scatter(x='SPH', y='UOM', title='asasasas')
        # Splitting the data into training data and testing data
        Xp_train, Xp_test, Zp_train, Zp_test = train_test_split(Xp, Zp, test_size=0.2, random_state=42)
        regressor.fit(Xp_train, Zp_train)
        # prediction on training data
        training_data_prediction_pdf1 = regressor.predict(Xp_train)

        r2p_train1 = metrics.r2_score(Zp_train, training_data_prediction_pdf1)
        test_data_prediction_pdf1 = regressor.predict(Xp_train)
        r2p_test1 = metrics.r2_score(Zp_train, test_data_prediction_pdf1)

        input_data_as_numpy_array_pdf1 = np.asarray(SPH)
        input_data_reshaped_pdf1 = input_data_as_numpy_array_pdf1.reshape(-1, 1)
        prediction_pdf1 = regressor.predict(input_data_reshaped_pdf1)

        print("UOM")
        print(prediction_pdf1[0])
        import createPdfFile
        a=createPdfFile.b #a is byte
        #1 Mib 1048.576 kb
        #boş pdf 993 byte
        a = a * 0.001 #a byte to kb
        a = (a*993)/1048.756
        prediction_pdf[0] = prediction_pdf[0] / a  #a is kb
        print("user when generate pdf file")
        print("UOC",prediction_pdf[0])
        prediction_pdf1[0] = prediction_pdf1[0] / a
        print("UOM",prediction_pdf1[0])
        dictionary = {
            "id": "62f3575ab51f8a773cde8ed1",
            "SPH": SPH,
            "UOM": prediction_pdf1[0][0],
            "UOC": prediction_pdf[0][0],
            "IsPdfSend" : 1
        }

        out_file = open("data.json", "w")
        json_object = json.dump(dictionary, out_file, indent=6)
        out_file.close()

        datalistSPH = []
        dataListUOM = []
        dataListUOC = []
        dataListPDF = []
        datalistSPH.append(SPH)
        dataListUOM.append(prediction_pdf1)
        dataListUOC.append(prediction_pdf)
        dataListPDF.append(1)

        """d = [datalistSPH, dataListUOM, dataListUOC, dataListPDF]
        export_data = zip_longest(*d, fillvalue='')
        with open('PdfUsageMemory.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("SPH", "UOM", "UOC", "PDF"))
            wr.writerows(export_data)
        myfile.close()
        """
        plt.figure(figsize=(10, 10))
        sns.countplot(x='SPH', data=pdf_dataset)
        plt.title('Submission per hour Distribution')
        plt.show()

        plt.figure(figsize=(10, 10))
        sns.distplot(pdf_dataset['UOM'])
        plt.title('Usage of memory')
        plt.show()

        plt.figure(figsize=(10, 10))
        sns.countplot(x='UOC', data=pdf_dataset)
        plt.title('Usage of cpu')
        plt.show()




while (True):
    time.sleep(1)
    if (lastValue != rabbitmqReceiver.x or pdfValue != rabbitmqReceiver.y):
        lastValue = rabbitmqReceiver.x
        pdfValue = rabbitmqReceiver.y
        main_(lastValue,pdfValue)

