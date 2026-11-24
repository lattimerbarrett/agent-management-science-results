import json,pathlib,itertools,collections,time
raw=json.loads(pathlib.Path('workspace/agent3_T280_P12_allorbits.json').read_text())['base_orbits']
Ss=[sum(1<<x for x in o['base']) for o in raw]
M=[[[[0]*7 for ep in range(2)] for h in range(128)] for o in raw]
wit={};count=collections.Counter();start=time.time()
for r in range(7):
 for piv in itertools.combinations(range(7),r):
  non=[j for j in range(7) if j not in piv];free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
  for z in range(1<<len(free)):
   B=[1<<p for p in piv]
   for k,(i,j) in enumerate(free):
    if z>>k&1:B[i]^=1<<j
   H=[0]
   for b in B:H += [x^b for x in H]
   ns=[h for h in range(1,128) if all((h&b).bit_count()%2==0 for b in B)]
   offs=[0]
   for j in non:offs += [x^(1<<j) for x in offs]
   for o in offs:
    F=sum(1<<(x^o) for x in H);cs=[(s&F).bit_count() for s in Ss];count[r]+=1
    for h in ns:
     ep=(h&o).bit_count()%2
     for i,c in enumerate(cs):
      if c>M[i][h][ep][r]:
       M[i][h][ep][r]=c
       if r>=4:wit[str((i,h,ep,r))]=[B,o,c]
 print('r',r,'flats',count[r], 'time',time.time()-start,flush=True)
res=[]
for i,ob in enumerate(raw):
 allbounds=[]
 for h in range(1,128):
  MM=[]
  for ep in range(2):
   MM.append([max((1<<(d-r))*M[i][h][ep][r] for r in range(max(0,d-3),min(d,6)+1)) for d in range(8)])
  for ep in range(2):
   best=max((MM[ep][a]+MM[ep][b],a,b) for a in range(2,8) for b in range(2,8) if a+b<=9)
   bound=MM[1-ep][7]+best[0]
   allbounds.append({'normal':h,'inner_side':ep,'bound':bound,'pairdims':best[1:],'M':MM})
 hist=collections.Counter(t['bound'] for t in allbounds)
 print(ob['type'],'bounds',dict(sorted(hist.items())),flush=True)
 res.append({'type':ob['type'],'max_bound':max(t['bound'] for t in allbounds),'bounds':allbounds})
out={'flat_counts':dict(count),'M':M,'witnesses':wit,'results':res}
pathlib.Path('workspace/agent3_E256_threeflat382_splitcaps.json').write_text(json.dumps(out,indent=2))
pathlib.Path('workspace/agent3_E256_threeflat382_splitcaps.py').write_text(pathlib.Path('scratchpad.py').read_text())
