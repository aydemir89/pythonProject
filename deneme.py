import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import json

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

input_data = (101)

insurance_dataset.plot.scatter(x='SPH', y='UOC', title='asasasas')
#splitting feature and target

#X=insurance_dataset.drop(columns='scores', axis = 1)
#Y=insurance_dataset['scores']
X = insurance_dataset['SPH'].values.reshape(-1, 1)
Y = insurance_dataset['UOC'].values.reshape(-1, 1)
Z = insurance_dataset['UOM'].values.reshape(-1, 1)

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
print("UOC")
print(prediction[0])

"""-----------------------------------------------------"""
insurance_dataset.plot.scatter(x='SPH', y='UOM', title='asasasas')
#Splitting the data into training data and testing data
X_train,X_test,Z_train,Z_test=train_test_split(X,Z,test_size=0.2, random_state=42)
#Model Training
#Linear Regression
regressor.fit(X_train,Z_train)
#prediction on training data
training_data_prediction1 = regressor.predict(X_train)
# R squared value
r2_train1 = metrics.r2_score(Z_train,training_data_prediction1)
test_data_prediction1 = regressor.predict(X_test)
r2_test1 = metrics.r2_score(Z_test,test_data_prediction1)

input_data_as_numpy_array1=np.asarray(input_data)
input_data_reshaped1 = input_data_as_numpy_array.reshape(-1,1)
prediction1 = regressor.predict(input_data_reshaped1)

print("UOM")
print(prediction1[0])

dictionary = {
        "id" : "62f3575ab51f8a773cde8ed1",
        "SPH" : input_data,
        "UOM" : prediction1[0][0],
        "UOC" : prediction[0][0],
}
out_file = open("data.json","w")
json_object=json.dump(dictionary,out_file,indent=6)
out_file.close()








plt.figure(figsize=(10,10))
sns.countplot(x='SPH',data=insurance_dataset)
plt.title('Submission per hour Distribution')
plt.show()

plt.figure(figsize=(10,10))
sns.distplot(insurance_dataset['UOM'])
plt.title('Usage of memory')
plt.show()

plt.figure(figsize=(10,10))
sns.countplot(x='UOC',data=insurance_dataset)
plt.title('Usage of cpu')
plt.show()









