from sys import argv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score

predict = "Debt Indicator"
if len(argv) == 2:
  predict = argv[1]

print("Trying to predict " + predict)

df = pd.read_csv("cleaned_data.csv")
# Scikit learn pca,normailze before hand
X = df[["# Lines added","# Lines added (over 3)","# Lines added (over 5)","# Lines removed","# Lines removed (over 3)","# Lines removed (over 5)","# Hunks count","# Files committed","# Contributors committed (over 3)","# Contributors committed (over 5)","% Comments Delta","% Duplicated lines Delta"]].copy()
y = df[predict]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# decision tree
dtree = tree.DecisionTreeClassifier()
dtree.fit(X_train, y_train)
y_pred = dtree.predict(X_test)

print('Decision Tree Accuracy: ' + str(accuracy_score(y_test, y_pred))+" with depth of "+str(dtree.get_depth()))

# random forest
forest = RandomForestClassifier()
forest.fit(X_train, y_train)
y_pred = forest.predict(X_test)

print('Random Forest Accuracy: ' + str(accuracy_score(y_test, y_pred)))

# linear regression
reg = LinearRegression()
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)

print('Linear regression MAE: ' + str(mean_absolute_error(y_test, y_pred)))
print('Linear regression MSE: ' + str(mean_squared_error(y_test, y_pred)))
print('Linear regression R2: ' + str(r2_score(y_test, y_pred)))
