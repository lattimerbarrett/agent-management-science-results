import sys,itertools,time,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_derivations import *
n=4;gs=generators(n);nv=len(gs)
def bitvec(D):
 z=0
 for h,p in enumerate(D):
  for w,c in p.items():
   if c%2:z^=1<<(h*n**len(w)+sum((x-1)*n**(len(w)-q-1) for q,x in enumerate(w)))
 return z
class Basis:
 def __init__(self):self.rows={};self.ds=[]
 def insert(self,D):
  z=bitvec(D);c=0
  while z:
   q=(z&-z).bit_length()-1
   if q in self.rows:z^=self.rows[q][0];c^=self.rows[q][1]
   else:
    c^=1<<len(self.ds);self.rows[q]=(z,c);self.ds.append(D);return
 def coords(self,D):
  z=bitvec(D);c=0
  while z:
   q=(z&-z).bit_length()-1
   assert q in self.rows
   z^=self.rows[q][0];c^=self.rows[q][1]
  return c
B2=Basis()
for i,j in itertools.combinations(range(nv),2):B2.insert(deriv_bracket(gs[i],gs[j]))
d2=len(B2.ds);print('d2',d2,flush=True)
c2={(i,j):B2.coords(deriv_bracket(gs[i],gs[j])) for i,j in itertools.combinations(range(nv),2)}
B3=Basis()
for D in B2.ds:
 for E in gs:B3.insert(deriv_bracket(D,E))
d3=len(B3.ds);print('d3',d3,flush=True)
c3={(i,j):B3.coords(deriv_bracket(D,E)) for i,D in enumerate(B2.ds) for j,E in enumerate(gs)}
def bits(z):
 while z:
  q=(z&-z).bit_length()-1;yield q;z^=1<<q
pairs=list(itertools.combinations(range(d2),2));pairidx={p:k for k,p in enumerate(pairs)};offset=d3*nv
rels={}
for u in range(d2):
 for a,b in itertools.combinations(range(nv),2):
  z=0
  for q in bits(c3[u,a]):z^=1<<(q*nv+b)
  for q in bits(c3[u,b]):z^=1<<(q*nv+a)
  for v in bits(c2[a,b]):
   if v!=u:z^=1<<(offset+pairidx[tuple(sorted((u,v)))])
  while z:
   q=(z&-z).bit_length()-1
   if q in rels:z^=rels[q]
   else:rels[q]=z;break
print('L4upperdim',offset+len(pairs)-len(rels),'relationrank',len(rels),flush=True)
B4=Basis()
for D in B3.ds:
 for E in gs:B4.insert(deriv_bracket(D,E))
print('Johnson4rank',len(B4.ds),flush=True)
# Original core W0152 maps n4 indices(0,1,9,3)
D=deriv_bracket(deriv_bracket(gs[0],gs[1]),gs[9]);c=B3.coords(D);z=sum(1<<(q*nv+3) for q in bits(c))
while z:
 q=(z&-z).bit_length()-1
 if q in rels:z^=rels[q]
 else:break
print('seed residue nonzero?',bool(z),'residueweight',z.bit_count(),flush=True)
