import sys,time
sys.path.insert(0,'workspace')
from agent3_arithmetic_fields import data,X
from sage.all import pari
from pathlib import Path
for c in [4,8,16,32,64]:
 p,ell,r,e,P=data(c)
 poly=pari(str(P.as_expr()).replace('X','x').replace('**','^'))
 t=time.time();nf=pari.nfinit(poly)
 pi=pari.Mod(pari('x'),poly);u=1+pi;v=1-pi**(c-1)+pi**(2*c-2)
 primes=pari.idealprimedec(nf,2)
 print('c',c,'degree',e,'numprimes',len(primes),'Hilbert(v,u)',pari.nfhilbert(nf,v,u,primes[0]),'seconds',time.time()-t,flush=True)
