import json,pathlib,collections,time
raw=json.loads(pathlib.Path('workspace/agent3_T272_q224_P24_allseeds.json').read_text())['seeds']
valid={tuple(sorted((p&63)|(((p>>8)&1)<<6) for p in a['Q'])) for a in raw};assert len(valid)==896
q=lambda x:sum((x>>(2*i)&1)*(x>>(2*i+1)&1) for i in range(3))&1
vlist=[v for v in range(64) if q(v)];maps=[]
for v in vlist:maps.append([x^((q(x^v)^q(x)^q(v))*v) for x in range(128)])
for i in range(6):maps.append([x^(((x>>i)&1)<<6) for x in range(128)])
assert all(all(q(x)==q(g[x]) for x in range(128)) for g in maps)
seed=next(iter(valid));seen={seed};queue=collections.deque([seed]);start=time.time()
while queue:
 a=queue.popleft()
 for g in maps:
  b=tuple(sorted(g[x] for x in a))
  assert b in valid
  if b not in seen:seen.add(b);queue.append(b)
print('orbit',len(seen),'of',len(valid),'generators',len(maps),'seconds',time.time()-start)
pathlib.Path('workspace/agent3_T272_cubic_single_orbit.json').write_text(json.dumps({'orbit_size':len(seen),'valid_caps':len(valid),'seed':seed,'maps':maps,'all_caps':list(seen)},indent=2))
pathlib.Path('workspace/agent3_T272_cubic_single_orbit.py').write_text(pathlib.Path(__file__).read_text())
