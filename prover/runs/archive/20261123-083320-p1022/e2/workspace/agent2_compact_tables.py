"""Recomputes and verifies the compact P2/P3 root tables used in proof.
No pickle files are used. The full lower certificate separately proves
root completeness by ideal-membership/finite-grid certificates.
"""
import sympy as S
import importlib.util
from pathlib import Path

def module(filename,name):
 spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(filename))
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def actual(m,parts):
 eq,vs=m.equations(parts)
 gb=S.groebner(eq,*reversed(vs))
 out=set()
 for values in S.solve_poly_system(list(gb),*reversed(vs)):
  sol=dict(zip(reversed(vs),values));row=[]
  for i,r in enumerate(parts):
   poly=S.Integer(1)
   for j in range(1,r+1):
    for k,base in enumerate(m.B[j]):poly+=sol[S.Symbol(f'u{i}_{j}_{k}')]*base
   row.append(S.expand(poly))
  out.add(tuple(row))
 return out

def verify(m,parts,expected):
 expected={tuple(S.expand(f) for f in row) for row in expected}
 assert actual(m,parts)==expected,(parts,actual(m,parts),expected)
 print(parts,':',len(expected),'roots verified')

def main():
 m=module('agent2_p2_chow.py','p2');s=m.h+m.x
 Z=S.Integer(1);P=1-s;R=1+s;P2=1-2*s;R2=1+2*s
 for parts in ((1,1),(1,2)):
  verify(m,parts,[(Z,Z),(P,R)])
 verify(m,(1,1,1),[(Z,Z,Z),(P,R,Z),(Z,P,R),(P2,Z,R2)])
 m=module('agent2_p3_chow.py','p3');s=m.h+m.x;u=s*s-m.h*m.x
 Z=S.Integer(1);P=1-s;R=1+s;M=1+s+u;N=1-s+u;P2=1-2*s;R2=1+2*s
 for b in range(2,5):verify(m,(1,b),[(Z,Z),(P,M)])
 for b in (2,3):verify(m,(2,b),[(Z,Z),(P,M),(N,R)])
 for b in (2,3):verify(m,(1,b,1),[(Z,Z,Z),(P,M,Z),(Z,N,R)])
 verify(m,(1,2,2),[(Z,Z,Z),(P,M,Z),(Z,N,R),(Z,P,M),(P2,Z,R2+4*u)])
 verify(m,(2,1,2),[(Z,Z,Z),(Z,P,M),(N,R,Z),(P2,Z,R2+4*u),(P2+4*u,Z,R2)])
 print('All compact tables match exact computed Chern roots.')
if __name__=='__main__':main()
