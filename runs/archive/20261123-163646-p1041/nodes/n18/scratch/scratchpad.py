import json,pickle,time
D=json.load(open('aperiod308_model.json'));n=D['n'];a=D['counts'];fm=[0]*4;j=0
for t,num in enumerate(a):
 for _ in range(num):
  for i in range(4):
   if t>>i&1:fm[i]|=1<<j
  j+=1
S=set()
for m in fm:
 A=set();x=m
 while True:
  A.add(x)
  if x==0:break
  x=(x-1)&m
 S^=A
print('weight',len(S),'periods',[v for v in range(1,1<<n) if all(x^v in S for x in S)])
V=pickle.load(open('experiments/e2/agent3_veronese_%d_5.pkl'%n,'rb'));B={};K=[]
ss=sorted(S)
for i,p in enumerate(ss):
 v=V[p];c=1<<i
 while v:
  j=v.bit_length()-1
  if j in B:v^=B[j][0];c^=B[j][1]
  else:B[j]=(v,c);break
 if v==0:K.append(c)
cl=[]
for p,v in enumerate(V):
 if p in S:continue
 c=0
 while v:
  j=v.bit_length()-1
  if j not in B:break
  v^=B[j][0];c^=B[j][1]
 if v==0:cl.append((p,c))
print('kernel',len(K),'closure extra',len(cl))
print('Gram nonzero',[(i,j) for i in range(len(K)) for j in range(i) if (K[i]&K[j]).bit_count()%2])
import pickle
pickle.dump((n,ss,K),open('308_kernel.pkl','wb'))
if cl:
 p,c=cl[0];H={ss[i] for i in range(len(ss)) if c>>i&1}|{p}
 L=H|{x|(1<<n) for x in (H^S)}
 print('liftedweight',len(L));json.dump({'n':n+1,'support':sorted(L)},open('lift310.json','w'))
json.dump({'n':n,'support':ss},open('308_seed.json','w'))