import json,pathlib,sys,itertools,collections
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese,kernel
obj=json.loads(pathlib.Path('workspace/agent3_T296_k12_P12_base_candidates.json').read_text());B=obj['base'];assert len(obj['P6'])==1;A=obj['P6'][0]
S=sorted(x+(u<<8) for x in B for u in range(4));v=veronese(10,5);u4=veronese(11,4);u5=veronese(11,5);u6=veronese(11,6)
D={}
for j,p in enumerate(S):
 z=v[p];c=1<<j
 while z:
  h=z.bit_length()-1
  if h in D:z^=D[h][0];c^=D[h][1]
  else:D[h]=(z,c);break
assert 272-len(D)==11
res=[];hist=collections.Counter()
for direction in [1,2,3]:
 for bs in range(64):
  P=[]
  for j,p in enumerate(A):
   # Representatives of the two cosets of <direction> in F2²
   rep=next(x for x in range(1,4) if x!=direction) if bs>>j&1 else 0
   P += [p+(rep<<8),p+((rep^direction)<<8)]
  assert len(set(P))==12
  z=0
  for p in P:z^=v[p]
  c=0;rem=0
  for h in sorted(D,reverse=True):
   if z>>h&1:z^=D[h][0];c^=D[h][1]
  if z:continue
  H=set(P)|{S[j] for j in range(272) if c>>j&1};F=sorted(H|{x^1024 for x in set(S)^H});assert len(F)==296
  sy=0
  for p in F:sy^=u6[p]
  assert sy==0
  K4=kernel(F,u4);K5=kernel(F,u5);odd=sum((a&b).bit_count()%2 for a in K4 for b in K5)
  hist[(len(K4),len(K5),bool(odd))]+=1
  res.append({'direction':direction,'offsets':bs,'P':P,'support':F,'K4':len(K4),'K5':len(K5),'odd':odd})
print('valid',len(res),'hist',hist)
pathlib.Path('workspace/agent3_T296_k12_all.json').write_text(json.dumps({'histogram':{str(k):v for k,v in hist.items()},'results':res},indent=2))
pathlib.Path('workspace/agent3_T296_k12_all.py').write_text(pathlib.Path(__file__).read_text())
