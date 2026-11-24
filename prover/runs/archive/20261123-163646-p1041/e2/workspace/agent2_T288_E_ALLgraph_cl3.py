import pathlib,itertools
s=pathlib.Path('workspace/agent2_T288_E_ALLgraph_cl3.py').read_text()
start=s.index("D=json.load")
s=s[:start]+'''d3=veronese(11,3);d5=veronese(11,5);uu3=veronese(12,3);uu5=veronese(12,5);hist=collections.Counter();lhist=collections.Counter();hits=[];t=time.time();count=0
def process(S,typ):
 global count
 count+=1
 K3=kernel(S,d3);K5=kernel(S,d5);ext,rk=closure(set(S),d3);odd=sum((a&b).bit_count()%2 for a in K3 for b in K5);hist[typ,len(K3),len(K5),len(ext),bool(odd)]+=1
 if ext or odd:hits.append({'seed':count,'support':S,'extra':[p for p,c in ext],'odd':odd})
 if len(K5)>12:
  B={}
  for j in range(-1,11):insert(B,sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1))
  X=[]
  for x in K5:
   z=insert(B,x)
   if z:X.append(z)
  assert len(X)==1
  U=[p|(((X[0]>>i)&1)<<11) for i,p in enumerate(S)];KU=kernel(U,uu5);ue,rk=closure(set(U),uu3);lhist[len(KU),len(ue)]+=1
  if ue:hits.append({'lift_of':count,'support':U,'extra':[p for p,c in ue]})
'''
a=pathlib.Path('workspace/agent3_T288_E256_P16_contained.py').read_text();s+=a[a.index('raw='):a.index('  K5=kernel(F,u5)')]+"  process(F,obj['type'])\n"
s+='''print('count',count,'hist',hist,'lhist',lhist,'hits',len(hits),'sec',time.time()-t)
json.dump({'count':count,'hist':{str(k):v for k,v in hist.items()},'lhist':{str(k):v for k,v in lhist.items()},'hits':hits},open('workspace/agent2_T288_E_ALLgraph_cl3.json','w'));pathlib.Path('workspace/agent2_T288_E_ALLgraph_cl3.py').write_text(pathlib.Path(__file__).read_text())
'''
pathlib.Path('workspace/agent2_T288_E_ALLgraph_cl3_full.py').write_text(s)
exec(compile(s,__file__,'exec'))
