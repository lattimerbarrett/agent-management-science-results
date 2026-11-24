"""High precision checks of the root-barrier inequalities at rational fixed spectra."""
import mpmath as mp
from itertools import product
mp.mp.dps=80
nodes=[-mp.mpf(8)/7,-mp.mpf(1),mp.mpf(0),mp.mpf(3)/7,mp.mpf(5)/7,mp.mpf(1)]
gaps=[(nodes[1],nodes[2]),(nodes[3],nodes[4])]
be=-mp.mpf(120)/343
q=lambda t:t**3-t-be/3
p=lambda t:t**3-t-2*be/3
qp=lambda t:3*t*t-1
P=lambda t:mp.fprod(t-u for u in nodes)
C=mp.mpf(100)

def check_at(xi):
    hp=[mp.fprod(t-u for j,u in enumerate(xi) if i!=j) for i,t in enumerate(xi)]
    g1=[-p(t)*hp[i]/P(t) for i,t in enumerate(xi)]
    g2=[-q(t)*hp[i]/P(t) for i,t in enumerate(xi)]
    assert min(g1+g2)>0
    Gam=[[mp.mpf(0) for i in xi] for k in xi]
    for k,t in enumerate(xi):
        Gam[k][k]=sum(1/(t-u) for j,u in enumerate(xi) if j!=k)-sum(1/(t-u) for u in nodes)+(qp(t)/p(t)+qp(t)/q(t))/2
        for i,u in enumerate(xi):
            if i!=k:Gam[k][i]=-(g1[i]/g1[k]+g2[i]/g2[k])/(2*(t-u))
    # Both H=sum Ui are bounded above. Left H has Ui'=e^-Ct/(t-a),
    # and right H has Ui'=-e^Ct/(b-t). Test diagonal connection Hessians.
    for side in ['left','right']:
        d1=[];d2=[]
        for i,t in enumerate(xi):
            a,b=gaps[i]
            if side=='left':
                first=mp.exp(-C*t)/(t-a);second=first*(-C-1/(t-a))
            else:
                first=-mp.exp(C*t)/(b-t);second=first*(C+1/(b-t))
            d1.append(first);d2.append(second)
        for i in range(len(xi)):
            val=d2[i]-sum(d1[k]*Gam[k][i] for k in range(len(xi)))
            assert val<0,(side,xi,i,val)

if __name__=='__main__':
    fractions=[mp.mpf('1e-20'),mp.mpf('1e-10'),mp.mpf('.01'),mp.mpf('.25'),mp.mpf('.5'),mp.mpf('.75'),mp.mpf('.99'),1-mp.mpf('1e-10'),1-mp.mpf('1e-20')]
    for ts in product(fractions,repeat=2):
        check_at([a+t*(b-a) for (a,b),t in zip(gaps,ts)])
    print('Both root-barrier connection Hessians strictly negative at all 81 high-precision points, including endpoint distances 1e-20.')
