import itertools,sys,json,time
sys.path.insert(0,'workspace');from agent4_checker import dec
out=[]
for n,D in [(5,2),(5,3),(6,4)]:
 fs=[sum(1<<v for v in c) for c in itertools.combinations(range(n),D)];d=D-1
 counts=[0]*(d+1);closure=[0]*(d+1);st=time.time()
 for bits in range(1,1<<len(fs)):
  F=tuple(sorted(f for i,f in enumerate(fs) if bits>>i&1))
  results=[dec(F,k) for k in range(d+1)]
  assert results[d]==results[d-1]
  for k,v in enumerate(results):counts[k]+=v
  faces={0}
  for f in F:
   g=f
   while g:
    faces.add(g);g=(g-1)&f
  for f in fs:
   if f in F:continue
   if not all((f^(1<<v)) in faces for v in range(n) if f>>v&1):continue
   G=tuple(sorted(F+(f,)))
   for k,valid in enumerate(results):
    if valid:assert dec(G,k);closure[k]+=1
 item={'n':n,'d':d,'nonempty_families':(1<<len(fs))-1,'k_decomp_counts':counts,'full_boundary_checks':closure,'seconds':time.time()-st};out.append(item);print(item,flush=True)
json.dump(out,open('workspace/agent3_top_parameter_check_result.json','w'))
with open('scratchpad.py') as src,open('workspace/agent3_top_parameter_check.py','w') as dst:dst.write(src.read())
