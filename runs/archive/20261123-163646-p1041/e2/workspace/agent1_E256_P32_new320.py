import sys,itertools,json,pathlib,time,collections,random
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def basis(cols):
 B={};K=[]
 for i,v in enumerate(cols):
  c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:K.append(c)
 return B,K

def red(v,B):
 c=0;r=0
 while v:
  k=v.bit_length()-1
  if k not in B:r^=1<<k;v^=1<<k;continue
  v^=B[k][0];c^=B[k][1]
 return r,c
obj=next(x for x in json.load(open('workspace/agent4_boundary256_orbits.json')) if x['solvable']);S=sorted({(p&63)|((p>>3)&64) for p in obj['support']});X,r=closure(set(S),veronese(7,2));E0=sorted(p for p,c in X);B,K=basis(veronese(7,3)[p] for p in S);RR=[red(veronese(7,3)[p],B)[0] for p in E0];B,KB=basis(RR);assert len(KB)==7;C=[0]
for u in KB:C +=[z^u for z in C]
subspaces={};start=time.time()
for a,b,c in itertools.combinations(C[1:],3):
 if a^b==c or (a|b|c).bit_count()!=8:continue
 key=tuple(sorted([a,b,c,a^b,a^c,b^c,a^b^c]));subspaces.setdefault(key,(a,b,c))
print('SUBSPACES',len(subspaces),'time',time.time()-start,flush=True)
T=sorted(p|(r<<7) for p in S for r in range(8));v10=veronese(10,5);BT,KT=basis(v10[p] for p in T);v11=veronese(11,5);hist=collections.Counter();results=[];random.seed(32011);cases=[]
for ss,abc in enumerate(subspaces.values()):
 for off in range(256):cases.append((ss,abc,off))
random.shuffle(cases)
for count,(ss,abc,off) in enumerate(cases[:10000]):
 a,b,c=abc;I=[j for j in range(16) if (a|b|c)>>j&1];P=[]
 for ii,j in enumerate(I):
  n=((a>>j)&1)|(((b>>j)&1)<<1)|(((c>>j)&1)<<2);assert n
  for r in range(8):
   if (r&n).bit_count()%2==((off>>ii)&1):P.append(E0[j]|(r<<7))
 assert len(P)==32;vv=0
 for p in P:vv^=v10[p]
 rem,co=red(vv,BT);assert not rem
 H=P+[p for j,p in enumerate(T) if co>>j&1];G=sorted(set(H)^set(p|1024 for p in H)^set(p|1024 for p in T));assert len(G)==320
 BG,KG=basis(v11[p] for p in G);nz=sum((u&v).bit_count()%2 for u in KG for v in KG);hist[(len(KG),bool(nz))]+=1
 if nz or len(KG)>=15:
  cl,r=closure(set(G),v11);ans={'subspace':ss,'abc':abc,'offset':off,'support':G,'K5':len(KG),'Gram_nonzero':nz,'cl5extra':len(cl)};results.append(ans)
  if cl:ans['closure_witness']=[cl[0][0],cl[0][1]]
  print('INTERESTING',count,len(KG),nz,len(cl),flush=True)
 if count%1000==0:print(count,dict(hist),'time',time.time()-start,flush=True)
json.dump({'subspaces':len(subspaces),'totalcases':len(cases),'tested':min(10000,len(cases)),'hist':{str(k):v for k,v in hist.items()},'results':results},open('workspace/agent1_E256_P32_new320.json','w'));pathlib.Path('workspace/agent1_E256_P32_new320.py').write_text(pathlib.Path(__file__).read_text());print('DONE',dict(hist),len(results),time.time()-start)
