import pandas as pd
from sklearn.covariance import empirical_covariance
import math

df = pd.read_csv("cleaned_data.csv")
# Clusteranalysis
s = df[["dmm_unit_size","dmm_unit_complexity","dmm_unit_interfacing","# Churn","# Churn (over 3)","# Churn (over 5)","# Lines added","# Lines added (over 3)","# Lines added (over 5)","# Lines removed","# Lines removed (over 3)","# Lines removed (over 5)","# Hunks count","# Files committed","# Contributors committed (over 3)","# Contributors committed (over 5)","Complexity","% Comments","% Duplicated lines","SQALE","Coverage","SQALE Delta","Complexity Delta","% Comments Delta","% Duplicated lines Delta","Debt Indicator"]].copy()
s.astype(int)
cov = empirical_covariance(s)
for i, row in enumerate(cov):
    for j, cell in enumerate(row):
        if not math.isnan(cell) and i != j:
            p = s[s.columns[i]].corr(s[s.columns[j]])
            if (abs(p) > 0.3):
                # Covariance matrix, remove correlating stuff: over time data and lines removed, added etc. Over 0.3 seems to be a good measure to further look into
                print(s.columns[i] + " to "+ s.columns[j] + ": "+ str(p))
