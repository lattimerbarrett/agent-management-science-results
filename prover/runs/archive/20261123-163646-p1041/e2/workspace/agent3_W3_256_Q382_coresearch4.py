import itertools,collections,json,pathlib
p='workspace/agent3_W3_256_Q382_coresearch.json';d=json.load(open(p));S=set(d['core']);G=collections.defaultdict(list)
for piv in itertools.combinations(range(7),4):
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
   if len(S&{x^o for x in H})!=7:continue
   for h in ns:G[h,(h&o).bit_count()%2].append([B,o])
print('4flat7count',sum(len(a) for a in G.values())//7)
good=[]
for h in range(1,128):
 for ep in (0,1):
  a=d['flats'].get(str((h,ep,6)),[]);b=G[h,1-ep]
  if a and b:good.append([h,ep,len(a),len(b)])
print('good',good)
d['fourflats7']={str(k):v for k,v in G.items()};d['good4']=good
pathlib.Path('workspace/agent3_W3_256_Q382_coresearch4.json').write_text(json.dumps(d,indent=2))
pathlib.Path('workspace/agent3_W3_256_Q382_coresearch4.py').write_text(pathlib.Path('scratchpad.py').read_text())
