"""Diagnostic: Johnson-image ranks for McCool rank 3, not for IA_3.
Imports actual sparse tensor derivation arithmetic from agent3.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from agent3_derivations import basis,bracket
from sympy import divisors,mobius

def run(p):
 n=3
 gs=[{(i,(j,i)):1,(i,(i,j)):p-1} for i in range(n) for j in range(n) if i!=j]
 bs=gs; ranks=[len(bs)]
 for d in range(2,8):
  bs=basis((bracket(a,b,n,p) for a in gs for b in bs),p)
  ranks.append(len(bs))
 witt=[int(2*sum(mobius(k)*3**(d//k) for k in divisors(d))//d) for d in range(1,8)]
 if p>3:assert ranks==[6,6,16,36,96,231,618]
 assert witt==[6,6,16,36,96,232,624]
 print(p, 'image',ranks,'abstract almost-direct gr',witt)
 return ranks
if __name__=='__main__':
 for p in [1000003,1000033,2,3]:run(p)
