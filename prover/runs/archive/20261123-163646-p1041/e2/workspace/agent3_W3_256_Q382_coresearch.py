import itertools,collections,json,pathlib,time
S=[]
for a in range(16):
 x=[a>>i&1 for i in range(4)];q=[x[0]*x[1],x[0]*x[2],x[0]*x[3]^x[1]*x[2]]
 S.append(a+sum(v<<(4+j) for j,v in enumerate(q)))
ss=sum(1<<a for a in S);F=collections.defaultdict(list);cnt=collections.Counter()
for piv in itertools.combinations(range(7),3):
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
   mask=sum(1<<(x^o) for x in H);c=(mask&ss).bit_count();cnt[c]+=1
   if c in (6,7):
    for h in ns:F[h,(h&o).bit_count()%2,c].append([B,o])
print('core',S,'3flatcounts',dict(sorted(cnt.items())))
good=[]
for h in range(1,128):
 for ep in (0,1):
  a=F[h,ep,6];b=F[h,1-ep,7]
  if a and b:good.append([h,ep,len(a),len(b)])
print('goodhalfpairs',good)
pathlib.Path('workspace/agent3_W3_256_Q382_coresearch.json').write_text(json.dumps({'core':S,'good':good,'flats':{str(k):v for k,v in F.items()}},indent=2))
pathlib.Path('workspace/agent3_W3_256_Q382_coresearch.py').write_text(pathlib.Path('scratchpad.py').read_text())
