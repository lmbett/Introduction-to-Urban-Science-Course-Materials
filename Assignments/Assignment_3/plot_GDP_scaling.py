import csv
from pylab import *
import matplotlib.pyplot as plt

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

city=[]
pop=[]
gdp=[]
roads=[]
poproads=[]
product=[]

gg=open('gdp_simple.csv', 'r')
readerg=csv.reader(gg,delimiter=',')

f=csv.writer(open('GDP_roads_simple.csv','w'))

count=0

for rowg in readerg:
    if len(rowg) == 0:
        continue
    name=rowg[0]
    popg=rowg[1]
    gdpg=rowg[2]

    g=open('roads_simple.csv', 'r')
    reader=csv.reader(g,delimiter=',')
    flag=0

    for row in reader:
        if len(row) == 0:
            continue
        nm=row[0].lstrip()

        if (name==nm and name!='Madera'):
            flag=1
            city.append(name)
            pop.append(float(popg))
            gdp.append(float(gdpg))
            roads.append(float(row[2]))
            poproads.append(float(row[1]))
            prod=float(gdpg)*float(row[2])/float(popg)**2
            product.append(prod)
            count+=1


print ('There were ',count,' cities')
g.close()
gg.close()

xx=np.log10(pop)
yy=np.log10(gdp)

plt.plot(xx,yy,color='green',marker='o',ms=10,ls='None',alpha=0.3)

gradient, intercept, r_value, var_gr, var_it = linreg(xx,yy)
print("Gradient=", gradient, ", 95 % CI = [",gradient- 2.*np.sqrt(var_gr),",",gradient+2.*np.sqrt(var_gr),"]")
print("intercept=", intercept, ", 95 % CI = [",intercept- 2.*np.sqrt(var_it),",",intercept+2.*np.sqrt(var_it),"]")
print("R-squared", r_value)


tt=xx
tt.sort()
fitx=arange(float(tt[0])-.1,float(tt[-1])+.1,0.1,dtype=float)
fity=intercept + fitx*gradient
fityy=intercept-0.27 +7/6*fitx
plt.plot(fitx,fityy,'y-', linewidth=4, alpha=1.0,label=r'theory')
plt.plot(fitx,fity,'r-', linewidth=2, alpha=1.0,label=r'best fit')

plt.xlabel('Population')
plt.ylabel('US Metropolitan GDP ')
#str='scaling_GDP.png'
#savefig(str)
        #,dpi=400)
plt.show()



