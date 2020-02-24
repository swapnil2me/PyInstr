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
dataLocation = r"D:\Swapnil\OneDrive - Indian Institute of Science\001_Project_Data\003_PhD_Presentations\07_Thesis_Chapters\07_DRGN\DRGN_03\24_Annealing_in_atmosphere"
#r"D:\Swapnil\OneDrive - Indian Institute of Science\001_Project_Data\003_PhD_Presentations\07_Thesis_Chapters\07_DRGN\DRGN_03\22_RVG_InAir_Varying_Pressure\alpha_1.00bar"
paramDict = {'instClass':'KT2461',
             'address':'169.254.0.1',
             'source_channel':'a',
             'sourceVolt':0.05,
             'gate_channel':'b',
             'gateVolt':5,
             'dataPoints':100,
             'dataLocation':dataLocation,
             'experintName':'CurrentAnneal'}

rvg = expr.CurrentAnneal(paramDict,verbose = False)
rvg.setExperiment()
# try:
for i in range(1):
    (df,fileName) = rvg.startExperiment(saveData=True)
    print(df)
    print(df.columns)
    f, ax = plt.subplots(figsize=(10, 8))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    df.plot(x="timeStamp",y="Rsd_Ohm",ax=ax,colormap='gist_rainbow')
    if not os.path.exists(os.path.join(rvg.dataLocation,"Plots")):
        os.makedirs(os.path.join(rvg.dataLocation,"Plots"))

    figPath = os.path.join( os.path.join(rvg.dataLocation,"Plots"),
                            '{}.svg'.format(fileName.split('csv')[0][:-1]))
    plt.savefig(figPath)
    plt.close("all")
# except:
#     rvg.closeExperiment()


rvg.closeExperiment()



## Ploting reference
#https://pandas.pydata.org/pandas-docs/version/0.12/cookbook.html#cookbook-plotting
