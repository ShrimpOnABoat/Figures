#!/usr/bin/python

# import our packages
import sys
import matplotlib as mpl
mpl.use('tkagg')
import pandas as pd
import numpy as np
#import seaborn as sns
import matplotlib.style
import matplotlib.pyplot as plt
from cycler import cycler
from scipy import stats

# load the data
# 2 files with the same name, extensions txt and param
# read param first, then txt
# Figure type: IC50, trypan blue, growth curve
# MultiIndex columns: 1 or 2 (?)
# axis labels and log or not
# multi plot (in case there's a lot of data
# There should be default values for everything

# Print usage
Def usage():
    print("Usage: Figures.py filename")
    print("There must be a filename.txt and filename.param in the same directory")

# Default values
Figure_type = 'errorbar' # Other types : https://chartio.com/learn/charts/essential-chart-types-for-data-visualization/
Delimiteur = ';'
Index_number = [0]
Figure_number = 1
Relative_values = 0 # if 1, values and errors are relative to the first values
Xlabel = 'Concentrations (µM)'
Ylabel = 'Viability (%)'
Xscale = 'linear'
Legend_loc = 0
Stats = 0
Color_map = "tab20"

# liste des marqueurs préférés
marks = "ovX^s+*12d"

filename = sys.argv[1]
if filename == "":
    usage()
# retrieve the parameters
fparam = open(filename+".param")
for ligne in fparam:
    if (ligne.split(' ')[0] == 'Figure_type'):
        Figure_type = ligne.split(' ')[1][:-1]
    if (ligne.split(' ')[0] == 'Delimiteur'):
        Delimiteur = ligne.split(' ')[1][:-1]
    if (ligne.split(' ')[0] == 'Color_map'):
        Color_map = ligne.split(' ')[1][:-1]
    if (ligne.split(' ')[0] == 'Index_number'):
        Index_number = [*range(0,int(ligne.split(' ')[1]),1)]
    if (ligne.split(' ')[0] == 'Figure_number'):
        Figure_number = int(ligne.split(' ')[1])
    if (ligne.split(' ')[0] == 'Relative_values'):
        Relative_values = int(ligne.split(' ')[1])
    if (ligne.split(' ')[0] == 'Xlabel'):
        Xlabel = ' '.join(ligne.split(' ')[1:])
    if (ligne.split(' ')[0] == 'Ylabel'):
        Ylabel = ' '.join(ligne.split(' ')[1:])
    if (ligne.split(' ')[0] == 'Xscale'):
        Xscale = ligne.split(' ')[1][:-1]
    if (ligne.split(' ')[0] == 'Legend_loc'):
        Legend_loc = int(ligne.split(' ')[1])
    if (ligne.split(' ')[0] == 'Stats'):
        Stats = int(ligne.split(' ')[1])
fparam.close()

# stats
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6813708/ : The Student's t test is used to compare the means between two groups, whereas ANOVA is used to compare the means among three or more groups
def stars(p):
    if p < 0.0001:
        return "****"
    elif (p < 0.001):
        return "***"
    elif (p < 0.01):
        return "**"
    elif (p < 0.05):
        return "*"
    else:
        return "ns"

# Color map
if (Color_map == "viridis"):
    colors = plt.cm.viridis(np.linspace(0, 1, 10))
elif (Color_map == "plasma"):
    colors = plt.cm.plasma(np.linspace(0, 1, 10))
elif (Color_map == "rainbow"):
    colors = plt.cm.rainbow(np.linspace(0, 1, 10))
elif (Color_map == "brg"):
    colors = plt.cm.brg(np.linspace(0, 1, 10))
elif (Color_map == "tab10"):
    colors = plt.cm.tab10(np.linspace(0, 1, 10))
else:
    colors = plt.cm.tab20(np.linspace(0, 1, 20))

############
# Errorbar #
############

if(Figure_type=="errorbar"):
    data = pd.read_csv(filename + '.txt', sep = Delimiteur, index_col=Index_number)

    plt.figure(figsize=(8,5))
    plt.gca().set_prop_cycle(cycler('color', colors))

    if(len(Index_number)>1):
        gp = data.groupby(level=0, sort=False)
        moyennes = gp.mean().transpose()
        erreur_std = gp.std(ddof=0).transpose()
        if(Relative_values==1):
            moyennes_norm = moyennes/moyennes.iloc[0]
            erreur_norm = ((erreur_std/moyennes)**2+(erreur_std.iloc[0]/moyennes.iloc[0])**2)**0.5*moyennes_norm
            i = 0
            for row in data.index.unique(level=0):
                plt.errorbar(moyennes_norm.index.astype('float64'), moyennes_norm[row],
                             yerr=erreur_norm[row], fmt=marks[i]+'-', label=row, elinewidth=.5,
                             capsize=3, capthick=.5)
                i=i+1 % len(marks)
        else:
            i = 0
            for row in data.index.unique(level=0):
                plt.errorbar(moyennes.index.astype('float64'), moyennes[row],
                             yerr=erreur_std[row], fmt=marks[i]+'-', label=row, elinewidth=.5,
                             capsize=3, capthick=.5)
                i=i+1 % len(marks)

    plt.xscale(Xscale)
    plt.xticks([float(x) for x in moyennes.index.values[1:]],[float(x) for x in moyennes.index.values[1:]])
    plt.legend(loc=Legend_loc, fontsize=10)
    plt.xlabel(Xlabel, fontsize=10)
    plt.ylabel(Ylabel, fontsize=10)

    plt.savefig(filename+".pdf", dpi=1200, format='pdf')

############
# barchart #
############

if(Figure_type=="barchart"):
    data = pd.read_csv(filename + '.txt', sep = Delimiteur, index_col=Index_number)

    # figure
    if(len(Index_number)>1):
        gp = data.groupby(level=0, sort=False)
        if(Relative_values==1):
            moyennes = gp.mean().transpose()

            erreur_std = gp.std(ddof=0).transpose()
            moyennes_norm = moyennes/moyennes.iloc[0]
            erreur_norm = ((erreur_std/moyennes)**2+(erreur_std.iloc[0]/moyennes.iloc[0])**2)**0.5*moyennes_norm
            moyennes = moyennes_norm.transpose()
            erreur_std = erreur_norm.transpose()
        else:
            moyennes = gp.mean()
            erreur_std = gp.std(ddof=0)
    graph = moyennes.plot.bar(yerr=erreur_std, ecolor='black', capsize=5, color=colors, sort_columns=True)

# statistics
    if(Stats==1):
        j=0
        ydelta = .05 * abs(plt.ylim()[0] - plt.ylim()[1])
        for i in data.index.levels[0]:
            z, pval = stats.ttest_ind(data[data.columns[0]][i], data[data.columns[1]][i])
            print (i + ": " + str(pval))

            y_max = ydelta+max(moyennes[moyennes.columns[0]][j]+erreur_std[erreur_std.columns[0]][j], moyennes[moyennes.columns[1]][j]+erreur_std[erreur_std.columns[1]][j])

            plt.annotate("", xy=(j-.125, y_max), xycoords='data', xytext=(j+.125, y_max), textcoords='data', arrowprops=dict(arrowstyle="-", ec='black', connectionstyle="bar,fraction=0.2"))
            plt.text(j, y_max+ydelta, stars(pval), horizontalalignment='center', verticalalignment='center')
            j = j+1
        plt.ylim(plt.ylim()[0], plt.ylim()[1]+3.5*ydelta)
    plt.xticks(rotation='horizontal')
    plt.xlabel(Xlabel, fontsize=10)
    plt.ylabel(Ylabel, fontsize=10)
    plt.legend(loc=Legend_loc, fontsize=10)
    #plt.tight_layout()

    plt.savefig(filename+".pdf", dpi=1200, format='pdf')

###########
# scatter #
###########

# la première colonne contient l'axe des x, et les autres les valeurs en y. Il ne faut donc pas d'index
if(Figure_type=="scatter"):
    data = pd.read_csv(filename + '.txt', sep = Delimiteur, index_col=False).transpose()

    i=0
    for col in data.columns:
        plt.plot('Concentrations', 'Ligne 1', obj=data, fmt=marks[i] + '-', label='lolol')
        i = i + 1 % len(marks)
    plt.show()

