import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv("cleaned_data.csv")
# Scikit learn pca,normailze before hand
s = df[["# Lines added","# Lines added (over 3)","# Lines added (over 5)","# Lines removed","# Lines removed (over 3)","# Lines removed (over 5)","# Hunks count","# Files committed","# Contributors committed (over 3)","# Contributors committed (over 5)","% Comments Delta","% Duplicated lines Delta"]].copy()
s.astype(int)
sc = StandardScaler()
pca = PCA()
r = pca.fit_transform(sc.fit_transform(s))
# Adding a randomized variable to succesfully conclude, that it has no impact on the analysis
t = s.copy()
scr = StandardScaler()
pcar = PCA()
t["random"] = np.random.normal(0, 50, s.shape[0])
r2= pcar.fit_transform(scr.fit_transform(t))

custom_lines = [Line2D([0], [0], color="r", lw=4),
                Line2D([0], [0], color="b", lw=4),
                Line2D([0], [0], color="g", lw=4)]

fig, axs = plt.subplots(2, 2, gridspec_kw={"wspace": 0.8, "hspace": 0.5}, figsize=[8, 8])

axs[0, 0].set_title("Without feature random variable")
axs[0, 0].scatter(r[:,0],r[:,1], c=["b" if x == 0 else "g" if x < 0 else "r" for x in df["Debt Indicator"]])
axs[0, 1].set_title("With feature random variable")
axs[0, 1].scatter(r2[:,0],r2[:,1],c=["b" if x == 0 else "g" if x < 0 else "r" for x in df["Debt Indicator"]])
axs[0, 1].legend(custom_lines,["Higher", "Equal", "Lower"], loc="center right", bbox_to_anchor=(-0.25, 0.5), title="Debt change")
axs[1, 0].set_title("Explained variance")
axs[1, 0].set_xlabel("Principal Component")
axs[1, 0].set_ylabel("Variance")
axs[1, 0].plot(np.arange(len(pca.explained_variance_ratio_)), pca.explained_variance_ratio_, "tab:blue", label="Without random")
axs[1, 0].plot(np.arange(len(pcar.explained_variance_ratio_)), pcar.explained_variance_ratio_, "tab:red", label="With random")
axs[1, 0].legend(loc="lower left")
axs[1, 1].set_title("Impact of feature random varaible on PC")
axs[1, 1].set_xlabel("Principal Component")
axs[1, 1].set_ylabel("Impact")
axs[1, 1].bar(np.arange(len(pcar.components_)), [n[11] for n in pcar.components_])
fig.savefig("pca.png")
