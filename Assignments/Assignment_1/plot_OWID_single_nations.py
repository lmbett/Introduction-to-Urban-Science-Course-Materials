import csv
import scipy.optimize
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib.colors as colors
from colorsys import hsv_to_rgb
import datetime as dt

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def lin_fit(x, y):
    '''Fits a linear fit of the form mx+b to the data'''
    fitfunc = lambda params, x: params[0] * x    #create fitting function of form mx+b
    errfunc = lambda p, x, y: fitfunc(p, x) - y              #create error function for least squares fit

    init_a = 0.5                            #find initial value for a (gradient)
    init_p = np.array((init_a))  #bundle initial values in initial parameters

    #calculate best fitting parameters (i.e. m and b) using the error function
    p1, success = scipy.optimize.leastsq(errfunc, init_p.copy(), args = (x, y))
    f = fitfunc(p1, x)          #create a fit with those parameters
    return p1, f

def linreg(X, Y):
    """
        Summary
        Linear regression of y = ax + b
        Usage
        real, real, real = linreg(list, list)
        Returns coefficients to the regression line "y=ax+b" from x[] and y[], and R^2 Value
        """
    if len(X) != len(Y):  raise ValueError("unequal length")
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in zip(X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    a, b = (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
    meanerror = residual = 0.0
    for x, y in zip(X, Y):
        meanerror = meanerror + (y - Sy/N)**2
        residual = residual + (y - a * x - b)**2
    RR = 1 - residual/meanerror
    ss = residual / (N-2)
    Var_a, Var_b = ss * N / det, ss * Sxx / det
    return a, b, RR, Var_a, Var_b


f=open('urbanization-vs-gdp.csv', 'r',encoding='latin-1')
reader=csv.reader(f,delimiter=',')

country = 'United States'
window=30
norm = colors.Normalize(vmin=1, vmax=2*165)
sm = cm.ScalarMappable(norm, cmap=cm.Paired)
cnt = 0
c=0
nation=''
uall=[]
gall=[]
xall=[]
yall=[]
for row in reader:
    if (row[1]!='' and row[3]!='' and row[4]!='' and row[4].isdigit() and float(row[3])<99. ):
        #print(row[2],row[3],row[4])
        if (nation!=row[0]):
            #if (cnt>0 and ur[-1]<95 and nation=='France'): # and len(ur)>60):
            #or nation=='South Korea' or nation=='United States' or nation=='France' or nation=='Portugal' or nation=='China' or nation=='Germany' or nation=='Japan' or nation=='Brazil'
            if (cnt>0 and nation==country):#  or  nation=='South Korea'): # and len(ur)>60):
                xx=ur
                yy=np.log10(gdp)
                edge_color, color = sm.to_rgba(c), sm.to_rgba(c+1)
                edge_color=color
                cnt += 1
                c += 2
                
                for i in range(len(ur)):
                    if (yy[i]<2.5):
                        print(str(nation),year[i])
                    xall.append(xx[i])
                    yall.append(yy[i])
                
                plt.plot(xx,np.power(10,yy),marker='o',ms=6,ls='None',c='blue',markeredgecolor=edge_color,
                        markeredgewidth=1,alpha=0.8,label=str(nation))
            gdp=[]
            ur=[]
            year=[]
            pop=[]
            gdp.append(float(row[4]))
            ur.append(float(row[3]))
            year.append(int(row[2]))
            
            nation=row[0]
            #print(row[0],row[1],row[2],row[3],row[4])
            cnt=0
        else:
            gdp.append(float(row[4]))
            ur.append(float(row[3]))
            year.append(int(row[2]))
           
            cnt+=1
print("There are,",cnt,"years of data")

gradient, intercept, r_value, var_gr, var_it = linreg(xall,yall)
print("Gradient=", gradient, ", 95 % CI = [",gradient- 2.*np.sqrt(var_gr),",",gradient+2.*np.sqrt(var_gr),"]")
print("intercept=", intercept, ", 95 % CI = [",intercept- 2.*np.sqrt(var_it),",",intercept+2.*np.sqrt(var_it),"]")
print("R-squared", r_value**2)
    
# show models and best fit
tt=xall
tt.sort()
fitx=np.arange(float(tt[0])-0.01,float(tt[-1])+0.01,0.1,dtype=float)
fity=intercept + gradient*fitx

plt.plot(fitx,np.power(10, fity),'k-', linewidth=5, alpha=0.5)
plt.yscale('log')

plt.ylabel('GDPpc (2011)',fontsize=20)
plt.xlabel('Percent Urban',fontsize=20)
plt.tight_layout()
#plt.legend()
plt.savefig('Trajectories_' + country.replace(' ', '_') + '_OWID.pdf', format='pdf')
plt.show()
