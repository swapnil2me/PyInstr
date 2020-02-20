import sys
import os
sys.path.append(os.path.join(os.getcwd(),'lib'))

import instruments as inst
import experiments as expr

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns
sns.set()
#sns.axes_style("darkgrid")
#sns.axes_style("ticks")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8,'axes.facecolor': '#EAEAF2'})

paramDict = {'instClass':'KT2461',
             'address':'169.254.0.1',
             'source_channel':'a',
             'sourceVolt':0.05,
             'gate_channel':'b',
             'gateSweep':[-10,2.5,10],
             'dataLocation':r"D:\Swapnil\OneDrive - Indian Institute of Science\001_Project_Data\003_PhD_Presentations\07_Thesis_Chapters\07_DRGN\DRGN_03\07_RVG_test_nb",
             'experintName':'Rvg'}

rvg = expr.Rvg(paramDict)
rvg.setExperiment()
(df,fileName) = rvg.startExperiment()
rvg.closeExperiment()
f, ax = plt.subplots(figsize=(10, 8))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
df.plot(x="Vg(V).get",y="Rsd(Ohm)",ax=ax,colormap='gist_rainbow')

if not os.path.exists(os.path.join(rvg.dataLocation,"Plots")):
    os.makedirs(os.path.join(rvg.dataLocation,"Plots"))

figPath = os.path.join( os.path.join(rvg.dataLocation,"Plots"),
                        '{}.svg'.format(fileName.split('csv')[0][:-1]))
plt.savefig(figPath)
plt.show()


## Ploting reference
#https://pandas.pydata.org/pandas-docs/version/0.12/cookbook.html#cookbook-plotting
