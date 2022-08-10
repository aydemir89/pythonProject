import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import json
#import DataGenerator

#Data Collection & Analysis
insurance_dataset = pd.read_csv('UsageOfServers.csv')
#print(insurance_dataset.to_string())

#first 5 rows of the dataframe
insurance_dataset.head()
#number of rows and columns
insurance_dataset.shape
insurance_dataset.info()

#checking for missing values
insurance_dataset.isnull().sum()
# statistical measures
insurance_dataset.describe()
#print(insurance_dataset.describe())

input_data = (67)

insurance_dataset.plot.scatter(x='SPH', y='UOM', title='Scatterplot of hours and scores percentages')
#splitting feature and target

#X=insurance_dataset.drop(columns='scores', axis = 1)
#Y=insurance_dataset['scores']
X = insurance_dataset['SPH'].values.reshape(-1, 1)
Y = insurance_dataset['UOM'].values.reshape(-1, 1)

#Splitting the data into training data and testing data
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2, random_state=42)
#print(X.shape,X_train.shape,X_test.shape)


#Model Training
#Linear Regression
regressor = LinearRegression()
regressor.fit(X_train,Y_train)
print(regressor.intercept_)
#Model Evaluation
print(regressor.coef_)

#prediction on training data
training_data_prediction = regressor.predict(X_train)
# R squared value
r2_train = metrics.r2_score(Y_train,training_data_prediction)
print('R square value:', r2_train)

test_data_prediction = regressor.predict(X_test)
r2_test = metrics.r2_score(Y_test,test_data_prediction)
print('R square value:', r2_test)

input_data_as_numpy_array=np.asarray(input_data)
input_data_reshaped = input_data_as_numpy_array.reshape(-1,1)
prediction = regressor.predict(input_data_reshaped)
print(prediction[0])


#submisson kullanarak memory bulmak için


#id = DataGenerator.user


