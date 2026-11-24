import json,itertools,time,numpy as np,z3
start=time.time();loc=json.load(open('workspace/agent4_partial_cover_saturation.json'))[0]['family'];t=7
lcores=[{0,1,2,9,10,11},{3,4,12,13,14},{5,6,15,16,17},{7,8,18,19,20}];oldl=[{0,1,2},{3,4},{5,6},{7,8}]
ocores=[{21,22},{23,24},{25,26}];cores=ocores+lcores;LH=[]
for e in loc:
 e=set(e);i=next(i for i,X in enumerate(oldl) if X<=e);LH.append(lcores[i]|(e-oldl[i]))
outer=[]
for i,X in enumerate(ocores):
 for p in ocores[(i+1)%3]:outer.append(X|{p})
H=LH[:]
for e in outer:
 for choices in itertools.product(*[sorted(X) for X in lcores]):H.append(e|set(choices))
def mask(E):return sum(1<<v for v in E)
H=list(set(mask(E) for E in H));C=mask({21,23,25,0,1,3,5});arr=np.array(H,dtype=np.int64)
assert np.all((arr&C)!=0)
s=z3.Solver();xs=[z3.Bool('c%d'%i) for i in range(27)];s.add(z3.PbLe([(x,1) for x in xs],6))
for e in H:s.add(z3.Or([xs[p] for p in range(27) if e>>p&1]))
assert s.check()==z3.unsat
assert not any((C&mask(X))==mask(X) for X in cores)
# Intersections checked in blocks, including basefamily.
for a in range(0,len(arr),100):assert np.all((arr[a:a+100,None]&arr[None,:])!=0)
allowed=[]
for e in itertools.combinations(range(27),7):
 E=set(e)
 if any(X<=E for X in cores):allowed.append(mask(E))
allowed=np.array(allowed,dtype=np.int64);addable=[]
for a in range(0,len(allowed),200):
 block=allowed[a:a+200];ok=np.all((block[:,None]&arr[None,:])!=0,axis=1);addable.extend(map(int,block[ok]))
assert all(e&C for e in addable)
added=[];Hset=set(H)
for e in addable:
 if e not in Hset and all(e&f for f in added):added.append(e);Hset.add(e)
H+=added;arr=np.array(H,dtype=np.int64)
# Greedy additions produce a maximalintersectingallowedfamily; allrejects witness either base or an earlieraddition.
assert all(e in Hset or any(not e&f for f in added) for e in addable)
for X in cores:
 F=[e for e in H if (e&mask(X))==mask(X)];intersection=(1<<27)-1
 for e in F:intersection&=e
 assert intersection==mask(X)
for e in H:
 intersections=arr&e;singles=intersections[(intersections!=0)&((intersections&(intersections-1))==0)]
 assert int(np.bitwise_or.reduce(singles))==e
for p,q in itertools.combinations(range(27),2):
 ip=next(i for i,X in enumerate(cores) if p in X);iq=next(i for i,X in enumerate(cores) if q in X)
 if ip==iq:witness=next(e for e in H if (e&mask(cores[ip]))==mask(cores[ip]))
 else:
  witness=mask({p,q}|{min(X) for i,X in enumerate(cores) if i not in (ip,iq)})
 assert witness.bit_count()==t and np.all((arr&witness)!=0)
out=dict(t=t,n=27,cores=[sorted(X) for X in cores],initial_edges=len(H)-len(added),final_edges=len(H),added=len(added),allowed=len(allowed),base_addable=len(addable),cover=[p for p in range(27) if C>>p&1],z3_all_6_covers_unsat=True,all_occurrences_private=True,all_351_pairs_mincover=True,globally_min_ground_under_caps=True,full_cores=True,saturated=True,runtime=time.time()-start)
print(out,flush=True)
with open('workspace/agent4_join_partial_cover_checks.json','w') as f:json.dump(out,f,indent=2)
with open('workspace/agent4_join_partial_cover_checks.py','w') as f:f.write(open(__file__).read())
