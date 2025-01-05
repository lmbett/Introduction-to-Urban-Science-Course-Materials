from scipy import optimize
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def Y1(x):
    out = nMF*f1*x[0] + (1.-nMF)/2.
    return out

def Y2(x):
    out = nMF*(1.-f1)*x[1] + (1.-nMF)/2.
    return out

def G1(x):
    out = ( f1*x[0]**(1-sigmaS) + (1-f1)*(x[1]*T )**(1-sigmaS) )**(1/(1-sigmaS))
    return out

def G2(x):
    out =( f1*( x[0]*T )**(1-sigmaS) + (1-f1)*x[1]**(1-sigmaS) )**(1/(1-sigmaS))
    return out

def yw1(x): # as defined in Fujita et al
    out =  ( Y1(x)*G1(x)**(sigmaS-1) + Y2(x)*G2(x)**(sigmaS-1)*(T**(1-sigmaS)) )**(1/sigmaS)
    return out

def yw2(x): # as defined in Fujita et al
    out = ( Y1(x)*G1(x)**(sigmaS-1)*(T**(1-sigmaS)) + Y2(x)*G2(x)**(sigmaS-1) )**(1/sigmaS)
    return out

def fun(x):
    return ( ( x[0] -yw1(x) )**2 +( x[1] -yw2(x) )**2 )

def func(x):
    out = [x[0]-yw1(x)]
    out.append( x[1]-yw2(x) )
    return out

sigmaS=4.
T=1.3
tau=1./T
nMF=0.4


x=[1,1]

min=x
minimum=0.1

npoints=500

fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
for i in range(1, 2):
    T=T+0.1*(i-1)
    ax = fig.add_subplot(1, 1, i)
        #    ax.text(0.5, 0.5, str((2, 3, i)),
        #    fontsize=18, ha='center')

    a=[]
    b=[]
    
    for ii in range(41):
        f1=ii/40.
        minimum=0.1
        min=[1,1]
    
        x02 = fsolve(func,x)
        a.append(f1)
        b.append(x02[0]*G1(x02)**(-nMF)-x02[1]*G2(x02)**(-nMF))

    plt.axhline(y=0.,linewidth=1, color='k')
    plt.axvline(x=0.5,linewidth=1, color='k')

    titlestring=r'$T=$'+str(T)+',  '+r'$n_{MF}=$'+str(nMF)+',  '+r'$\sigma_S=$'+str(sigmaS)
    plt.title(titlestring)

    plt.ylabel(r'$y_{\omega_1}-y_{\omega_2}$',fontsize=20)
    plt.xlabel(r'$f_1$',fontsize=20)

    plt.plot(a,b,'b-',lw=5,alpha=0.5)
    plt.xlim(0, 1)

#plt.plot(xx1,yy1,'b-',lw=8,alpha=0.5)

plt.savefig('real_wage_difference_vs_f1.pdf', format='pdf',bbox_inches='tight')
#plt.tight_layout()
plt.show()

