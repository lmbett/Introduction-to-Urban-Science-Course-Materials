import numpy as np
import matplotlib.pyplot as plt

# Equation is
# R^3 + R_*^2 R - (A_0)^(3/2) N = 0


# set R_* and G/\epsilon; A_0 = (G/\epsilon)^(2/3), which has dimensions of an area. A_0 ~ 10 person per ha?
# cycle over N, with sufficiently large R_*

Rcrit=300. # in metres
A0 = 10000. # 1 hectare in m^2

Rsol=[]
Rsol1=[]
Rsol2=[]
Rsol3=[]
pop=[]

for N in range(1,2500):

    Rsol1.append( (A0**1.5/Rcrit**2 *N)**2 )
    Rsol2.append( (A0**0.5 * N**0.333)**2 )
    Rsol3.append( 2*(A0**1.5/Rcrit**2 *N**0.75)**2 )
    
    s=-(A0**1.5)*N
    coeff = [1.,0.,Rcrit**2,s] #p[0] is highest power, p[n] is x^0 coefficient.
    #coeff = [1.,0.,10.,100.]
    ss=np.roots(coeff)
    for j in range(len(ss)):
        if (ss.imag[j]==0.):
            pop.append(N)
            Rsol.append( (ss.real[j])**2 )
            #            print(ss.real[j])
            #            print(ss.imag[j])


Acrit=Rcrit**2

plt.loglog(pop,Rsol,'k-',lw=6,alpha=0.4)
plt.loglog(pop,Rsol1,'r--',alpha=0.5)
plt.loglog(pop,Rsol2,'g--',alpha=0.5)
plt.loglog(pop,Rsol3,'y-',alpha=1)

plt.loglog((1/10.,10**4.),(Rcrit**2,Rcrit**2),'k-')
plt.ylabel('Log Area',fontsize=20)
plt.xlabel('Log Population',fontsize=20)
plt.xlim(1,10**3.2)
plt.tight_layout()

plt.show()
