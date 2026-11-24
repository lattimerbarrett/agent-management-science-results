"""Exact rational smooth-pointed FZ rows and one-rational-tail correction, g=24."""
from fractions import Fraction
from functools import lru_cache
from math import factorial,comb
from collections import defaultdict

def make_scope(k0):
 from pathlib import Path
 s=(Path(__file__).parent/'fz_engine.py').read_text()
 s=s.replace('D=12','D=13').replace('k0=48',f'k0={k0}')
 s=s.replace('range(1,11)','range(1,16)')
 s=s.replace('def inv(x):return pow(x,P-2,P)','def inv(x):return Fraction(1,x)')
 s=s.replace('pow(-logA[n],j,P)','(-logA[n])**j').replace('%P','')
 ns={'Fraction':Fraction};exec(s,ns);return ns
S48=make_scope(48);S47=make_scope(47)
@lru_cache(None)
def core(k0,sig):
 S=S48 if k0==48 else S47
 return S['pmul'](S['E'],S['f'](sig))

def smooth(r,sig,aa):
 k0=46+len(aa);S=S48 if k0==48 else S47
 out=defaultdict(Fraction)
 def comps(n,l):
  if l==1:yield(n,);return
  for a in range(n+1):
   for rest in comps(n-a,l-1):yield(a,)+rest
 for mu,c in core(k0,sig).items():
  if sum(mu)>r:continue
  for exps in comps(r-sum(mu),len(aa)):
   co=c
   for a,e in zip(aa,exps):co*=(S['A'] if a==0 else S['B'])[e]
   if co:out[(mu,exps)]+=co
 return dict(out)

def tail(r,sig,a,b):
 out=defaultdict(Fraction);n1=sig.count(1)
 for m in range(n1+1):
  rem=list(sig)
  for _ in range(m):rem.remove(1)
  mult=(-1)**(a+b)*comb(n1,m)*factorial(m)
  for mu,c in core(47,tuple(rem)).items():
   e=r-1-sum(mu)
   if e<0:continue
   h=S47['B'][e+1] if (m+a+b)%2 else -S47['A'][e+1]
   if h:out[(mu,e)]+=mult*c*h
 return {m:c for m,c in out.items() if c}

