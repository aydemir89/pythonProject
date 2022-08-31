from typing import Optional
import mysql.connector
import mysql
import typer
import csv
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import typer
from rich.prompt import Prompt
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import rabbitmqSender
import rabbitmqReceiver
import DataGenerator


from rich.table import Table
from rich.console import Console
import json

import Database


app = typer.Typer()


user ="62f3575ab51f8a773cde8ed1"
a = Database.connection

@app.command()
def start(id: Optional[str] = None):
        typer.echo(f"Hello to AIops project")

        if(user == id):
            typer.echo(f"Hello to AIops project {id}")
        else:
            typer.echo(f"You have to enter your id so I can recognize you")

console = Console()


def show(table):
    table.add_column("#", style="dim", width=3, justify="center")
    table.add_column("id", min_width=20, justify="center")
    table.add_column("SPH", min_width=12, justify="center")
    table.add_column("UOM", min_width=12, justify="center")
    table.add_column("UOC", min_width=12, justify="center")
    table.add_column("IsPdfSend", min_width=12, justify="center")
    table.add_column("Payment", min_width=12, justify="center")
    table.add_column("SuggestedPayment", min_width=12, justify="center")
    table.add_column("Suggested UOM", min_width=12, justify="center")
    table.add_column("Suggested UOC", min_width=12, justify="center")
    table.add_column("CreatedAt", min_width=12, justify="center")


@app.command(short_help="shows last predicted data")
def printTable(table):
    f = open('data.json')
    data = json.load(f)

    f = open('Suggested.json')
    sd = json.load(f)
    show(table)

    table.add_row(f'[cyan]{1}[/cyan]', f'[cyan]{data["id"]}[/cyan]', f'[green]{data["SPH"]}[/green]',
                  f'[green]{data["UOM"]}[/green]', f'[green]{data["UOC"]}[/green]',
                  f'[green]{data["IsPdfSend"]}[/green]', f'[green]{data["paymentSystem"]}[/green]', f'[green]{data["SuggestedPayment"]}[/green]', f'[green]{data["CreatedAt"]}[/green]')

    console.print(table)


def AllPredictionRecords(table):
    connection = mysql.connector.connect(host='localhost',
                                         database='aiopsdb',
                                         user='root',
                                         password='root', auth_plugin='mysql_native_password')

    sql_select_Query = "SELECT * FROM aiopsdb.usageserver"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    show(table)

    for idx, row in enumerate(records, start=1):
        table.add_row(str(idx), f'[cyan]{row[0]}[/cyan]', f'[green]{row[1]}[/green]',f'[cyan]{row[2]}[/cyan]', f'[green]{row[3]}[/green]',f'[green]{row[4]}[/green]',f'[green]{row[5]}[/green]')

    console.print(table)

def YesPDFPredictionData(SPH):

    regressor = LinearRegression()

    pdf_dataset = pd.read_csv('PdfUsageMemory.csv')
    # pdf_dataset.head()
    # pdf_dataset.shape
    # pdf_dataset.info()
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
    # print('R square value:', r2p_test)

    input_data_as_numpy_array_pdf = np.asarray(SPH)
    input_data_reshaped_pdf = input_data_as_numpy_array_pdf.reshape(-1, 1)
    prediction_pdf = regressor.predict(input_data_reshaped_pdf)
    # print("UOC")
    # print(prediction_pdf[0])

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

    # print("UOM")
    # print(prediction_pdf1[0])
    """ import createPdfFile"""
    """a=createPdfFile.b"""  # a is byte
    # 1 Mib 1048.576 kb
    # boş pdf 993 byte
    a = 993
    a = a * 0.001  # a byte to kb
    a = (a * 993) / 1048.756
    prediction_pdf[0] = prediction_pdf[0] / a  # a is kb
    # print("user when generate pdf file")
    # print("UOC",prediction_pdf[0])
    prediction_pdf1[0] = prediction_pdf1[0] / a

    return prediction_pdf,prediction_pdf1

def NoPDFPredictionData(SPH):
    prediction1 = 0
    prediction = 0
    # Data Collection & Analysis

    regressor = LinearRegression()
    # PdfUsageMemory kullandığı kısım

    insurance_dataset = pd.read_csv('UsageOfServers.csv')

    # UsageOfServers.csv kullandığı#

    # first 5 rows of the dataframe
    # insurance_dataset.head()
    # number of rows and columns
    # insurance_dataset.shape
    # insurance_dataset.info()

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
    # print(regressor.intercept_)
    # Model Evaluation
    # print(regressor.coef_)

    # prediction on training data
    training_data_prediction = regressor.predict(X_train)
    # R squared value
    r2_train = metrics.r2_score(Y_train, training_data_prediction)
    # print('R square value:', r2_train)

    test_data_prediction = regressor.predict(X_test)
    r2_test = metrics.r2_score(Y_test, test_data_prediction)
    # print('R square value:', r2_test)

    input_data_as_numpy_array = np.asarray(SPH)
    input_data_reshaped = input_data_as_numpy_array.reshape(-1, 1)
    prediction = regressor.predict(input_data_reshaped)
    # print("UOC")
    # print(prediction[0])
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
    # print("UOM")

    return prediction,prediction1

@app.command()
def prediction():
    lastValue = 0
    pdfValue = 0
    rabbitmqReceiver.main()
    SuggestedPrediction = ""


    def Seperate():
        time.sleep(1)
        file = csv.DictReader(open('dataSet.csv', 'r'))
        datalistSPH = []
        dataListUOM = []
        dataListUOC = []
        dataListPDF = []
        dataListPDF2 = []
        dataListUser = []
        temp = []
        user = "62f3575ab51f8a773cde8ed1"
        for col in file:
            datalistSPH.append(col['SPH'])
            dataListUOM.append(col['UOM'])
            dataListUOC.append(col['UOC'])
            dataListPDF.append(col['PDF'])

        count = -1
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

        header = ['UserId', 'SPH', 'UOM', 'UOC', "PDF"]

        with open('PdfUsageMemory.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write the data
            writer.writerows(dataRowPdf1)

        with open('UsageOfServers.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write the data
            writer.writerows(dataRowPdf0)

    def main_(SPH, IsPdfSend, paymentSystem):

        SuggestedPrediction = paymentSystem

        if(IsPdfSend == 0):

            prediction,prediction1 = NoPDFPredictionData(SPH)

            if (prediction1[0] >= 100 or prediction[0] >= 100):
                prediction1[0] = 100
                prediction[0] = 100
            if (prediction1[0] <= 0 or prediction[0] <= 0):
                prediction1[0] = 0
                prediction[0] = 0

            if (SPH > 100 and SPH < 1000 and prediction1[0] == 100):
                SuggestedPrediction = "Bronze"  # free
            elif (SPH > 1000 and SPH < 2500 and prediction1[0] == 100):
                SuggestedPrediction = "Silver"  # bronze
            elif (SPH > 2500 and SPH < 10000 and prediction1[0] == 100):
                SuggestedPrediction = "Gold"  # silver
            elif (SPH > 100000 and prediction1[0] == 100):
                SuggestedPrediction = "Enterprise"  # gold

            dictionary = {
                "id": "62f3575ab51f8a773cde8ed1",
                "SPH": SPH,
                "UOM": prediction1[0][0],
                "UOC": prediction[0][0],
                "IsPdfSend": 0,
                "paymentSystem": paymentSystem,
                "SuggestedPayment": SuggestedPrediction,
                "CreatedAt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }

            out_file = open("data.json", "w")
            json_object = json.dump(dictionary, out_file, indent=6)
            out_file.close()

            """plt.figure(figsize=(10, 10))
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
    """

        elif(IsPdfSend == 1):

            prediction_pdf,prediction_pdf1 = YesPDFPredictionData(SPH)

            if (prediction_pdf1[0] >= 100 or prediction_pdf >= 100):
                prediction_pdf[0] = 100
                prediction_pdf1[0] = 100
            if (prediction_pdf1[0] <= 0 or prediction_pdf[0] <= 0):
                prediction_pdf[0][0] = 0
                prediction_pdf1[0][0] = 0
            # print("UOM",prediction_pdf1[0])


            if (SPH > 100 and SPH<1000 and  prediction_pdf[0] ==100):
                SuggestedPrediction = "Bronze" #free
            elif (SPH > 1000 and SPH<2500 and prediction_pdf[0] ==100 ):
                SuggestedPrediction = "Silver" #bronze
            elif (SPH > 2500 and SPH<10000 and prediction_pdf[0] ==100):
                SuggestedPrediction = "Gold"  #silver
            elif (SPH > 100000 and prediction_pdf[0] ==100):
                SuggestedPrediction = "Enterprise" #gold

            print("Suggested: ",SuggestedPrediction)

            dictionary = {
                "id": "62f3575ab51f8a773cde8ed1",
                "SPH": SPH,
                "UOM": prediction_pdf1[0][0],
                "UOC": prediction_pdf[0][0],
                "IsPdfSend": 1,
                "paymentSystem": paymentSystem,
                "SuggestedPayment": SuggestedPrediction,
                "CreatedAt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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

        """plt.figure(figsize=(10, 10))
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
        plt.show()"""

    while (True):
        time.sleep(0.1)
        #SPH = int(input("Enter the SPH you want to predict="))
        #print(f"Submission per hour: {SPH}!")

        #IsPdfSend = int(input("Will you send the forms as pdf?="))
        #print(f"PDF: {IsPdfSend}!")

        if (lastValue != rabbitmqReceiver.x or pdfValue != rabbitmqReceiver.y):

            time.sleep(1)
            lastValue = rabbitmqReceiver.x
            pdfValue = rabbitmqReceiver.y
            paymentSystem = rabbitmqReceiver.z
            DataGenerator.main(paymentSystem)
            Seperate()
            main_(lastValue, pdfValue, paymentSystem)

            predictionData = open('data.json')
            file = json.load(predictionData)

            if (file["paymentSystem"] != file["SuggestedPayment"]):
                DataGenerator.main(file["SuggestedPayment"])
                Seperate()
                if(file["IsPdfSend"] == 0):
                    console.print(YesPDFPredictionData(file["SPH"]))
                else:
                    console.print(NoPDFPredictionData(file["SPH"]))
                #main_(lastValue,pdfValue,file["SuggestedPayment"])


            rabbitmqSender.main()
            table = Table(show_header=True, header_style="bold blue", show_lines=True)
            printTable(table)
            SaveDatabase()




def SaveDatabase():
    delete = typer.confirm("do you want to save data")
    table = Table(show_header=True, header_style="bold blue", show_lines=True)
    if delete:
        Database.main()
        AllPredictionRecords(table)
    else:
        print("Not saved")




def updatePaymentSystem():
    """ SuggestedData = open('Suggested.json')
    data = json.load(SuggestedData)"""






if __name__ == "__main__":
    app()