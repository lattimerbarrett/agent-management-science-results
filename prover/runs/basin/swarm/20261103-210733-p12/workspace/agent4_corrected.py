import sys,time
sys.path.insert(0,'workspace')
from agent4_pairing import *
from functools import lru_cache
from sage.all import GF,matrix,vector,block_matrix,zero_matrix
F=GF(P)
@lru_cache(None)
def splits(a):
 c=Counter(a);ks=tuple(c);cs=tuple(c[k] for k in ks);out=[]
 for vv in product(*(range(v+1) for v in cs)):
  x=tuple(sorted((k for k,v in zip(ks,vv) for _ in range(v)),reverse=True))
  y=tuple(sorted((k for k,c0,v in zip(ks,cs,vv) for _ in range(c0-v)),reverse=True))
  z=1
  for c0,v in zip(cs,vv):z*=comb(c0,v)
  out.append((x,y,z))
 return out
@lru_cache(None)
def point(a,t,g):
 assert sum(a)+t==g-1
 out=0
 for x,y,z in splits(a):
  s=t+sum(y)
  if s==0:continue
  k=s-1
  if k==0:v=(2*g-2)*intersection(x,g)
  else:v=intersection(tuple(sorted(x+(k,),reverse=True)),g)
  out+=z*v
 return out%P

def mons(d):return [(a,d-sum(a)) for k in range(d+1) for a in partitions(k)]
def pair(x,y,g):return point(tuple(sorted(x[0]+y[0],reverse=True)),x[1]+y[1],g)

def factor(g):
 top=g-1;data={}
 for d in range(top+1):
  a=mons(d);b=mons(top-d)
  M=matrix(F,[[pair(x,y,g) for y in b] for x in a])
  rows=list(M.transpose().pivots());cols=list(M.pivots());
  data[d]={'basis':[a[i] for i in rows],'dual':[b[j] for j in cols],'pair':M.matrix_from_rows_and_columns(rows,cols)}
  print('factor',g,d,len(rows),flush=True)
 for d in range(top):
  A=data[d]['basis'];B=data[d+1]['dual']
  V=matrix(F,[[pair((x[0],x[1]+1),y,g) for y in B] for x in A])
  data[d]['psi']=(V*data[d+1]['pair'].inverse()).transpose()
 return data

t=time.time();A=factor(12);B=factor(13)
print('factor time',time.time()-t,flush=True)
# Degree11 source and degree12 target decomposed by A degree.
sizes11=[len(A[d]['basis'])*len(B[11-d]['basis']) for d in range(12)]
sizes12=[len(A[d]['basis'])*len(B[12-d]['basis']) for d in range(12)]
print('dimensions',sizes11,sum(sizes11),sizes12,sum(sizes12),flush=True)
blocks=[]
for d in range(12):
 row=[]
 for e in range(12):
  if d==e:
   v=matrix.identity(F,len(A[e]['basis'])).tensor_product(B[11-e]['psi'])
  elif d==e+1:
   v=A[e]['psi'].tensor_product(matrix.identity(F,len(B[11-e]['basis'])))
  else:v=zero_matrix(F,sizes12[d],sizes11[e])
  row.append(v)
 blocks.append(row)
M=block_matrix(F,blocks)
print('psi sum matrix',M.nrows(),M.ncols(),'rank',M.rank(),flush=True)
import pickle
pickle.dump((A,B,M),open('workspace/agent4_corrected.pkl','wb'))
