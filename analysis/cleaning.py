import pandas as pd
import numpy as np
from git import Repo

df = pd.read_csv("../crawler/data.csv")

def sqale_delta(row, metric):
    repo = Repo("../crawler/repo/"+row["project"])
    c = repo.commit(row["hash"])
    if len(c.parents) == 0:
        return 0 
    parent = c.parents[0]
    parent_Sqale = df.loc[df["hash"] == parent.hexsha]
    if len(parent_Sqale) == 0:
        return 0
    diff = parent_Sqale[metric]-row[metric]
    return diff.iloc[0]


# Data cleaning
df.fillna(0, inplace=True) # Filling empty rows
# Removing previous commit data
# e.g. Data is collected as # Churn over 5 and this contains # Churn over 3, but shouldnt
df["# Churn (over 5)"] = np.where((df["# Churn (over 5)"] != 0),df["# Churn (over 5)"]-df["# Churn (over 3)"],df["# Churn (over 5)"])
df["# Churn (over 3)"] = np.where((df["# Churn (over 3)"] != 0),df["# Churn (over 3)"]-df["# Churn"],df["# Churn (over 3)"])
df["# Lines added (over 5)"] = np.where((df["# Lines added (over 5)"] != 0),df["# Lines added (over 5)"]-df["# Lines added (over 3)"],df["# Lines added (over 5)"])
df["# Lines added (over 3)"] = np.where((df["# Lines added (over 3)"] != 0),df["# Lines added (over 3)"]-df["# Lines added"],df["# Lines added (over 3)"])
df["# Lines removed (over 5)"] = np.where((df["# Lines removed (over 5)"] != 0),df["# Lines removed (over 5)"]-df["# Lines removed (over 3)"],df["# Lines removed (over 5)"])
df["# Lines removed (over 3)"] = np.where((df["# Lines removed (over 3)"] != 0),df["# Lines removed (over 3)"]-df["# Lines removed"],df["# Lines removed (over 3)"])
df["# Contributors committed (over 5)"] = np.where((df["# Contributors committed (over 5)"] != 0),df["# Contributors committed (over 5)"]-df["# Contributors committed (over 5)"],df["# Contributors committed (over 5)"])
# This calculates a delta for a metric
df["SQALE Delta"] = df.apply(lambda row: sqale_delta(row, "SQALE"), axis = 1)
df["Complexity Delta"] = df.apply(lambda row: sqale_delta(row, "Complexity"), axis = 1)
df["% Comments Delta"] = df.apply(lambda row: sqale_delta(row, "% Comments"), axis = 1)
df["% Duplicated lines Delta"] = df.apply(lambda row: sqale_delta(row, "% Duplicated lines"), axis = 1)
# This is all about if the debt increases: 0 if it is 0, -1 if it is lower and1 if it has risen
df["Debt Indicator"] = df.apply(lambda row: -1 if row["SQALE Delta"] < 0 else 0 if row["SQALE Delta"] == 0 else 1, axis= 1)
df.to_csv("cleaned_data.csv")
