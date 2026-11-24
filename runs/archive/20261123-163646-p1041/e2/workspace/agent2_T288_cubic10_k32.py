import sys,json,pathlib,collections
sys.path.insert(0,'workspace');from agent3_lift_closure import veronese,closure

def kernel(S,vs):
 B={};out=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:out.append(c)
 return out
q=lambda x: ((x&1)*(x>>1&1))^((x>>2&1)*(x>>3&1))^((x>>4&1)*(x>>5&1))
T=[x for x in range(512) if q(x)];assert len(T)==224
v=veronese(9,5);u3=veronese(10,3);u5=veronese(10,5);u6=veronese(10,6)
K=kernel(T,v);assert len(K)==10
B={}
for i,p in enumerate(T):
 z=v[p];c=1<<i
 while z:
  k=z.bit_length()-1
  if k not in B:B[k]=(z,c);break
  z^=B[k][0];c^=B[k][1]
results=[]
for j,dirs in [(2,[0,2,4,6,7]),(3,[0,2,6,7,8])]:
 P=[0]
 for d in dirs:P +=[x^(1<<d) for x in P]
 assert len(P)==32 and all(q(p)==0 for p in P)
 z=0
 for p in P:z^=v[p]
 c=0
 while z:
  k=z.bit_length()-1
  if k not in B:break
  z^=B[k][0];c^=B[k][1]
 if z:results.append({'j':j,'solvable':False});continue
 H=set(P)|{p for i,p in enumerate(T) if c>>i&1};S=sorted(H|{p|512 for p in set(T)^H});assert len(S)==288
 syn=0
 for p in S:syn^=u6[p]
 assert syn==0
 K3=kernel(S,u3);K5=kernel(S,u5);odd=sum((a&b).bit_count()%2 for a in K3 for b in K5);ext,rk=closure(set(S),u3)
 rr={'j':j,'solvable':True,'K3':len(K3),'K5':len(K5),'odd':odd,'cl3extras':[p for p,c in ext],'support':S};results.append(rr)
print([{k:v for k,v in r.items() if k!='support'} for r in results]);json.dump({'sourceK5':len(K),'results':results},open('workspace/agent2_T288_cubic10_k32.json','w'));pathlib.Path('workspace/agent2_T288_cubic10_k32.py').write_text(pathlib.Path(__file__).read_text())
