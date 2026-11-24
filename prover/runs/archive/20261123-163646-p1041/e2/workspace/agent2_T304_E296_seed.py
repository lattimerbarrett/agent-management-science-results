import sys,json,pathlib,collections,itertools
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
D=json.load(open('workspace/agent2_T296_E_cl3_seed.json'));S=D['support'];E=D['cl3extra'];v=veronese(12,5);K=kernel(S+E,v);B={}
for k in K:
 z=k>>296
 while z:
  j=z.bit_length()-1
  if j in B:z^=B[j]
  else:B[j]=z;break
cs=[0]
for b in B.values():cs +=[c^b for c in cs]
print('relative',collections.Counter(c.bit_count() for c in cs))
# solve each P4
BB={}
for i,p in enumerate(S):
 z=v[p];c=1<<i
 while z:
  j=z.bit_length()-1
  if j in BB:z^=BB[j][0];c^=BB[j][1]
  else:BB[j]=(z,c);break
out=[]
for c in cs:
 if c.bit_count()!=4:continue
 P=[p for i,p in enumerate(E) if c>>i&1];z=0
 for p in P:z^=v[p]
 c=0
 while z:
  j=z.bit_length()-1;z^=BB[j][0];c^=BB[j][1]
 H=set(P)|{p for i,p in enumerate(S) if c>>i&1};T=sorted(H|{p|4096 for p in set(S)^H});assert len(T)==304
 K5=kernel(T,veronese(13,5));ext,rk=closure(set(T),veronese(13,4));out.append({'support':T,'K5':len(K5),'cl4extra':[p for p,c in ext]})
print('outputs',[(x['K5'],len(x['cl4extra'])) for x in out]);json.dump({'relative_enumerator':dict(collections.Counter(c.bit_count() for c in cs)),'outputs':out},open('workspace/agent2_T304_E296_seed.json','w'));pathlib.Path('workspace/agent2_T304_E296_seed.py').write_text(pathlib.Path(__file__).read_text())
