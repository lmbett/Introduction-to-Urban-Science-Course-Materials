import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as colors
from colorsys import hsv_to_rgb
from sklearn.metrics import r2_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster import hierarchy as hier
from scipy.spatial import distance as ssd

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


norm = colors.Normalize(vmin=1, vmax=2*len(range(1982,2015)))
sm = cm.ScalarMappable(norm, cmap=cm.Paired)
mk='o'

years=[]
cxx=[]
cyy=[]
avxx=[]
avyy=[]
gradients=[]
intercepts=[]
gerror=[]
r2s=[]

population=np.zeros((97,14))
congestion=np.zeros((97,14))

lxx=np.zeros((400,34))
lyy=np.zeros((400,34))

for i in range(1982,2015):
    count=0
    years.append(i)
    name=[]
    pop=[]
    AutoCommuters=[]
    DVMiles=[]
    ADVMiles=[]
    Tdollars=[]
    Tgallons=[]
    f=open('output.csv',encoding='utf-8', errors='ignore')
    reader=csv.reader(f,delimiter=',')
    cnt = (i-1982)
    #print(cnt)
    year=str(i)
    for row in reader:
        if (row[2]==year and row[0]!='Indio-Cathedral City CA' and row[0]!='Lancaster-Palmdale CA' and row[0]!='Poughkeepsie-Newburgh NY-NJ' and row[0]!='San Juan PR'):
            if (cnt>=19 and cnt<=32):
                jj=cnt-19
                population[count][jj]=float(row[3].replace(',',''))*1000.
                congestion[count][jj]=float(row[29].replace(',',''))*1000000.
            count+=1
            name.append(row[0])
            pop.append(float(row[3].replace(',',''))*1000.)
            AutoCommuters.append(float(row[5].replace(',',''))*1000.)
            DVMiles.append(float(row[6].replace(',',''))*1000.)
            ADVMiles.append(float(row[7].replace(',','').strip())*1000.)
            Tgallons.append(float(row[15].replace(',',''))*1000.)
            Tdollars.append(float(row[29].replace(',',''))*1000000.)

    xx=np.log10(pop)
    yy=np.log10(Tdollars)

    for j in range(len(pop)):
        lxx[j][cnt]=np.log10(pop[j])
        lyy[j][cnt]=np.log10(Tdollars[j])

    gradient, intercept, r_value, var_gr, var_it = linreg(xx,yy)
    print(year,'growth rate fit paramteres')
    print(gradient,", 95 % CI = [",gradient- 2.*np.sqrt(var_gr),",",gradient+2.*np.sqrt(var_gr),"]")
    print (intercept,", 95 % CI = [",(intercept- 2.*np.sqrt(var_it)),",",(intercept+2.*np.sqrt(var_it)),"]")
    print( "R-squared", r_value)

    gradients.append(gradient)
    intercepts.append(intercept)
    print('number of cities= ',len(pop))
f.close()

g=open('allgmp.csv',encoding='utf-8', errors='ignore')
greader=csv.reader(g,delimiter=',')

cc=1
noname=np.zeros(len(pop))

Gname=[]
Gcode=[]
Gpop=np.zeros((382,16))

f=open('population_MSAs.csv',encoding='utf-8', errors='ignore')
reader=csv.reader(f,delimiter=',')
c=0
for row in reader:
    if(len(row)>1):
        
        if(len(row[0])==5):
            Gname.append(row[1].split("(")[0])
            Gcode.append(int(row[0]))
            for i in range(2001,2015):
                ii=i-2001
                Gpop[c,ii]=row[2+ii]
            c+=1
f.close()

f=open('Real_GDP_Chained_MSAs.csv',encoding='utf-8', errors='ignore')
reader=csv.reader(f,delimiter=',')

c=0
RGDP=np.zeros((382,16))
for row in reader:
    if(len(row)>1):
        
        if(len(row[0])==5 and int(row[0])==Gcode[c]):
            for i in range(2001,2015):
                ii=i-2001
                RGDP[c,ii]=float(row[2+ii])*1000000.
            c+=1
f.close()

norm = colors.Normalize(vmin=1, vmax=2*len(range(2001,2015)))
sm = cm.ScalarMappable(norm, cmap=cm.Paired)
mk='o'
cnt=0
GDP=np.zeros((len(name),14))
noname=np.zeros((len(name)))
cc=0
for jj in range(len(Gname)):
    rr=Gname[jj]
    flag=0
    for i in range(len(name)):
        nn=name[i]
        state=nn.split(" ")[-1].split("-")[0]
        ll=len(nn.split(" "))
        if (ll >2):
           city=nn.split(" ")[0]+' '+nn.split(" ")[1].split("-")[0]
        else:
           city=nn.split(" ")[0]
        rr=rr.replace("/","-")
        if (city in rr and state in rr):
            #print(cc,city,state,rr)
            for j in range(14):
                    GDP[i][j]=RGDP[jj][j]
            noname[i]=1
            cc+=1
            flag=1

for j in range(14): # 2001-2014
    xxx=[]
    yyy=[]
    for i in range(len(name)):
        if (noname[i]==0):
            print('not matched',name[i])
        if (population[i][j]!=0 and congestion[i][j]!=0):
            yyy.append(congestion[i][j])
            xxx.append(GDP[i][j])

    xxxlog=np.log10(xxx)
    yyylog=np.log10(yyy)
    edge_color, color = sm.to_rgba(cnt), sm.to_rgba(cnt+1)
    edge_color='white'
    cnt += 2
    plt.plot(xxxlog,yyylog,marker='o',ms=10,ls='None',c=color,markeredgecolor=edge_color,markeredgewidth=1,alpha=0.4)


    gradient, intercept, r_value, var_gr, var_it = linreg(xxxlog,yyylog)
    print(2001+j,'reduced set fit paramteres')
    print(gradient,", 95 % CI = [",gradient- 2.*np.sqrt(var_gr),",",gradient+2.*np.sqrt(var_gr),"]")
    print (intercept,", 95 % CI = [",(intercept- 2.*np.sqrt(var_it)),",",(intercept+2.*np.sqrt(var_it)),"]")
    print( "R-squared", r_value)

    tt=xxxlog
    tt.sort()
    fitx=np.arange(9.5,12.5,0.1,dtype=float)
    fity=intercept + fitx*gradient
    fityy=intercept+0.1 +fitx

    plt.plot(fitx,fity,'-', c=color, linewidth=2, alpha=0.6)

plt.plot(fitx,fityy,'-', c='black', linewidth=2, alpha=0.6)

plt.xlabel('GDP (dollars)',fontsize=20)
plt.ylabel('congestion costs (dollars)',fontsize=20)
plt.tight_layout()

plt.show()
plt.clf()


SAMI=np.zeros((len(pop), len(gradients)))

for i in range(len(pop)):
    ssqrt=0.
    for j in range(len(gradients)):
        SAMI[i][j]=(lyy[i][j] - intercepts[j] -gradients[j]*lxx[i][j])
        ssqrt+=SAMI[i][j]**2
        if (abs(SAMI[i][j])>0.3):
            print(i,j,years[j],name[i],SAMI[i][j])
    plt.plot(years,SAMI[i][:],'-')

plt.xlabel('year',fontsize=20)
plt.ylabel('SAMIs',fontsize=20)
plt.tight_layout()

plt.show()
plt.clf()

###### samis
sam=[]
for i in range(len(pop)):
    sam.append(SAMI[i][-1])

#print(len(sam))

xs=[x for y, x in sorted(zip(sam, name))]
ys= [y for y, x in sorted(zip(sam, name))]
    
    
index = np.arange(len(ys))
bar_width = 0.4
opacity = 0.6
error_config = {'ecolor': '0.3'}
    
rects1 = plt.barh(index,ys, bar_width,
                      alpha=opacity,
                      color='b',
                      )
plt.yticks(index, xs, rotation='horizontal')
plt.margins(0.01)
plt.subplots_adjust(left=0.3)
plt.xlabel('SAMIs 2014',fontsize=20)
plt.tick_params(axis='y', which='major', labelsize=5)
label_size = 1
plt.rcParams['xtick.labelsize'] = label_size
plt.show()
plt.clf()



dist=np.zeros((len(pop), len(pop)))
#similarity matrix
for i in range(len(pop)):
    for j in range(len(pop)):
        dd=0.
        ni=0.
        nj=0.
        for k in range(len(gradients)):
            dd+=SAMI[i][k]*SAMI[j][k]
            ni+=SAMI[i][k]**2
            nj+=SAMI[j][k]**2
        dist[i][j]=1.-dd/np.sqrt(ni*nj) # this is the dis-similarity matrix
arr=dist

Z = hier.linkage(ssd.squareform(arr), method="complete")
hier.dendrogram(Z,labels=name) #leaf_rotation=0) #orientation='left',
plt.ylabel('dissimilarity',fontsize=20)
plt.xlabel('Metropolitan Areas',fontsize=20)
plt.show()


