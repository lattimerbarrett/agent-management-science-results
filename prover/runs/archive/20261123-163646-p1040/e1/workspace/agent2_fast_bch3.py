"""Integral class3 BCH coordinates (log1,2log2,12log3), exact Aut actions."""
import json,pickle
from pathlib import Path
from sage.all import Matrix,vector,ZZ,identity_matrix,zero_vector
from agent1_degree3 import mul,add,br,expand,coords,LP,L3,m
from agent1_degree3_closure import action_matrix,coords2,L2,pairs

n2=len(pairs);n3=len(L3);dim=m+n2+n3

def wordlog(w):
 ex=expand(w);f=[{u:x for u,x in ex.items() if len(u)==i} for i in range(1,4)];a,b,c=f
 diag={(i,i):x for (i,),x in a.items()};cube={(i,i,i):x for (i,),x in a.items()}
 q=add(add({u:2*x for u,x in b.items()},diag),mul(a,a),-1)
 cross={}
 for (i,j),x in b.items():cross=add(cross,{(i,i,j):x,(i,j,j):x}) if i!=j else add(cross,{(i,i,i):2*x})
 t={u:12*x for u,x in c.items()};t=add(t,cross,6);t=add(t,cube,2)
 t=add(t,add(mul(a,b),mul(b,a)),-6);t=add(t,add(mul(a,diag),mul(diag,a)),-3);t=add(t,mul(mul(a,a),a),4)
 return vector(ZZ,[a.get((i,),0) for i in range(m)]+coords2(q)+coords(t))

BR13=[]
for i in range(m):
 cols=[coords(br({(i,):1},p)) for p in L2]
 BR13.append(Matrix(ZZ,cols).transpose())

def br11(a,d):return vector(ZZ,[a[i]*d[j]-a[j]*d[i] for i,j in pairs])
def br13(a,b):
 ans=zero_vector(ZZ,n3);bb=vector(ZZ,b)
 for i,x in enumerate(a):
  if x:ans+=x*(BR13[i]*bb)
 return ans

def bch(x,y):
 a,b,c=x[:m],x[m:m+n2],x[m+n2:];d,e,f=y[:m],y[m:m+n2],y[m+n2:]
 ad=br11(a,d)
 v3=vector(ZZ,c)+vector(ZZ,f)+3*(br13(a,e)-br13(d,b))+br13(a,ad)-br13(d,ad)
 return vector(ZZ,list(vector(ZZ,a)+vector(ZZ,d))+list(vector(ZZ,b)+vector(ZZ,e)+ad)+list(v3))

def actions():
 cp=Path('workspace/agent2_fast_bch3_actions.pkl')
 if cp.exists():return pickle.loads(cp.read_bytes())
 d=json.load(open('workspace/agent2_nielsen_actions_n3.json'));iw=json.load(open('workspace/agent2_nielsen_inverse_words_n3.json'));out={}
 for i,s in enumerate(['T','P','I','C'],1):
  for sign,wds in [(1,d['actions'][s]['words']),(-1,iw[s])]:
   old=action_matrix(wds);cols=[list(wordlog(w)) for w in wds]
   for j in range(n2):cols.append([0]*m+old[:n2,j].list()+(3*old[n2:,j]).list())
   for j in range(n3):cols.append([0]*(m+n2)+old[n2:,n2+j].list())
   A=Matrix(ZZ,cols).transpose();out[sign*i]=A
  assert out[i]*out[-i]==identity_matrix(ZZ,dim)
 cp.write_bytes(pickle.dumps(out));return out

def actionword(w,acts=None):
 acts=actions() if acts is None else acts;A=identity_matrix(ZZ,dim)
 for i in w:A=A*acts[i]
 return A

def oldcoords(x):
 assert not any(x[:m]);b=x[m:m+n2];c=x[m+n2:]
 assert all(v%2==0 for v in b) and all(v%6==0 for v in c)
 return [v//2 for v in b]+[v//6 for v in c]

if __name__=='__main__':
 import random
 for _ in range(100):
  a=tuple(random.choice(list(range(1,10))+list(range(-9,0))) for i in range(5));b=tuple(random.choice(list(range(1,10))+list(range(-9,0))) for i in range(5))
  assert bch(wordlog(a),wordlog(b))==wordlog(a+b)
 print('PASS100exactBCHproductchecks')
 A=actions();print('PASS8fullactionsfreeinversechecks')
