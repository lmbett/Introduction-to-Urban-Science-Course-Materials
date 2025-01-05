import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as colors
from colorsys import hsv_to_rgb
from scipy.stats import entropy


def gini(list_of_values):
    sorted_list = sorted(list_of_values)
    height, area = 0., 0.
    for value in sorted_list:
        height += value
        area += height - value / 2.
    fair_area = height * len(list_of_values) / 2.
    return (fair_area - area) / fair_area





norm = colors.Normalize(vmin=1, vmax=130)
sm = cm.ScalarMappable(norm, cmap=cm.Paired)
cnt = 1
mk='o'
edge_color='white'

g=open('Neighborhood_MedianValuePerSqft_AllHomes_2016.csv', 'r') # this dataset ends at 2016.11
# the most recent data is here, but it seems to me has some bugs:  http://files.zillowstatic.com/research/public/Neighborhood/Neighborhood_MedianValuePerSqft_AllHomes.csv

reader=csv.reader(g,delimiter=',')

state='IL'
city='Chicago'

Median_P_sqft=[]
time_for_Inequality= 2008.+3./12. #from 1996.+1./12. to 2016+3./12. # this is the last date in this dataset 

for row in reader:
    if (row[3]==state and row[2]==city): # choose state and city (metro).
        color = sm.to_rgba(cnt)
        cnt+=1
        nn=[]
        time=[]
        ll=len(row)

        print('neighborhood: ',row[1],'; latest price/sq foot: ',row[ll-1])

        for i in range(len(row)-7):
            if (row[i+7]!=''):
                nn.append(float(row[i+7]))
                tt=1996. +float(i+1)/12.
                time.append(tt)

                if (tt==time_for_Inequality): 
                        Median_P_sqft.append(float(row[i+7]))


        plt.plot(time,nn,marker='o',ms=5,ls='None',c=color,markeredgecolor=edge_color,markeredgewidth=1,alpha=0.3,label=row[1])


#gini
print (time_for_Inequality,'gini=',gini(Median_P_sqft))

#entropy 
hist1 = np.histogram(Median_P_sqft, bins=20, density=False) # note that the frequencies (probability) depend on the number of bins
freq = hist1[0]
freq=freq/freq.sum()
H = 0
for i in freq:
    if (i >0.):
        H-= i * np.log(abs(i))
print ('Shannon Entropy, H=',H)




str_title='Price/ sq foot for Neighborhoods in '+city+','+state
plt.title(str_title)
plt.xlabel('time',fontsize=20)
plt.ylabel('median house price / sq foot',fontsize=20)
plt.xlim(1995,2018)
#plt.legend(loc=2)
plt.tight_layout()
plt.savefig('Neighborhoods_Chicago_Price_sq_foot.pdf', format='pdf')
#plt.show()
