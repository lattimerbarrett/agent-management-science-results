import json,pathlib,itertools,collections
raw=json.loads(pathlib.Path('workspace/agent3_T280_P12_allorbits.json').read_text())['base_orbits']
fl=[]
for piv in itertools.combinations(range(7),5):
 non=[j for j in range(7) if j not in piv];free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
 for z in range(1<<len(free)):
  B=[1<<p for p in piv]
  for h,(i,j) in enumerate(free):
   if z>>h&1:B[i]^=1<<j
  H=[0]
  for b in B:H += [x^b for x in H]
  offs=[0]
  for j in non:offs += [x^(1<<j) for x in offs]
  for o in offs:fl.append(set(x^o for x in H))
assert len(fl)==10668
out=[]
for obj in raw:
 S=set(obj['base']);hh=collections.Counter(len(S&H) for H in fl)
 out.append({'type':obj['type'],'5flat_intersections':dict(sorted(hh.items())),'maximum':max(hh)})
print(out)
pathlib.Path('workspace/agent3_E32_5flat_intersections.json').write_text(json.dumps(out,indent=2))
pathlib.Path('workspace/agent3_E32_5flat_intersections.py').write_text(pathlib.Path(__file__).read_text())
