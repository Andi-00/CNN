import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

plt.rcParams['pgf.rcfonts'] = False
plt.rcParams['font.serif'] = []
plt.rcParams['font.family'] = 'serif'
plt.rcParams['text.usetex'] = True
plt.rcParams['axes.formatter.useoffset'] = False
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['errorbar.capsize'] = 2
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.title_fontsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.1

#plt.rcParams['savefig.transparent'] = True
plt.rcParams['figure.figsize'] = (10, 6)


n_run = 9

data = pd.read_csv("./Network/network_output/run_1.{:02}/deltas.txt".format(n_run), delimiter = ",", names = ["Mass", "Distance", "Spin", "Eccentricity", "Seperation"])
# data = pd.read_csv("/hpcwork/cg457676/data/processed_parameter/pro_par9.csv", delimiter = ",", names = ["Mass", "Distance", "Spin", "Eccentricity", "Seperation"])

print(np.min(data), np.max(data))

sns.set_theme()

plot = sns.PairGrid(data, height = 2)

plot.map_upper(sns.kdeplot, fill = True)
plot.map_lower(sns.scatterplot, s = 5)
plot.map_diag(sns.histplot, kde=True)


plot.fig.suptitle('Correlations run 1.{:02}'.format(n_run))
plt.savefig("Corr_run_1.{:02}.png".format(n_run))

# plot.fig.suptitle('Correlations in run {}'.format(n_run))
# plt.savefig("./Network/network_output/run_{}/corr.png".format(n_run))