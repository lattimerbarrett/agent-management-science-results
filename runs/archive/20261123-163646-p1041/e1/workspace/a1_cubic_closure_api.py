import itertools,pickle,time,math,json,numpy as np
from sage.all import GF,matrix
from sage.coding.binary_code import weight_dist
cols=pickle.load(open('workspace/a1_cols13_degree5.pkl','rb'));N=8192;M3=(1<<sum(math.comb(13,j) for j in range(4)))-1

def closure_kernel(SS):
 S=set(SS);b3={}
 for x in SS:
  v=cols[x]&M3
  while v:
   p=v.bit_length()-1
   if p not in b3:b3[p]=v;break
   v^=b3[p]
 E=[]
 for x in range(N):
  if x in S:continue
  v=cols[x]&M3
  while v:
   p=v.bit_length()-1
   if p not in b3:break
   v^=b3[p]
  if not v:E.append(x)
 if not E:return E,[],{}
 b5={}
 for j,x in enumerate(SS):
  v=cols[x];c=1<<j
  while v:
   p=v.bit_length()-1
   if p not in b5:b5[p]=(v,c);break
   a,cc=b5[p];v^=a;c^=cc
 pp=sorted(b5,reverse=True);br={};ker=[]
 for j,x in enumerate(E):
  v=cols[x]
  for p in pp:
   if v>>p&1:v^=b5[p][0]
  c=1<<j
  while v:
   p=v.bit_length()-1
   if p not in br:br[p]=(v,c);break
   a,cc=br[p];v^=a;c^=cc
  if not v:ker.append(c)
 return E,ker,b5

