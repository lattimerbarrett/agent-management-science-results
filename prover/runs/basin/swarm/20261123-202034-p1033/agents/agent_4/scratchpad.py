import itertools,json,collections
cores=[set(range(4*i,4*i+4)) for i in range(6)];external={24,25}
Fs=[cores[0]|{4,24},cores[0]|{24,25}]
reps=[('A_same',Fs[0],cores[2]|{24,5}),('A_new',Fs[0],cores[2]|{24,12}),('B',Fs[1],cores[1]|{24,8})]
def sig(C,F,G):return tuple(sum((int(x in F)+2*int(x in G))==a for x in C) for a in range(4))
def certify(F,G,RF,RG):
 if sorted(sig(C,F,G) for C in cores)!=sorted(sig(C,RF,RG) for C in cores) or sig(external,F,G)!=sig(external,RF,RG):return None
 buckets=collections.defaultdict(list)
 for j,C in enumerate(cores):buckets[sig(C,RF,RG)].append(j)
 perm={}
 for C in cores:
  j=buckets[sig(C,F,G)].pop();D=cores[j]
  for a in range(4):
   S=sorted(x for x in C if int(x in F)+2*int(x in G)==a);T=sorted(x for x in D if int(x in RF)+2*int(x in RG)==a)
   assert len(S)==len(T);perm.update(zip(S,T))
 for a in range(4):
  S=sorted(x for x in external if int(x in F)+2*int(x in G)==a);T=sorted(x for x in external if int(x in RF)+2*int(x in RG)==a);perm.update(zip(S,T))
 assert set(perm)==set(range(26))==set(perm.values())
 assert {perm[x] for x in F}==RF and {perm[x] for x in G}==RG
 assert {frozenset(perm[x] for x in C) for C in cores}==set(map(frozenset,cores))
 return perm
records=[];counts=collections.Counter();fcounts=collections.Counter()
for ft,F in enumerate(Fs):
 for j in range(6):
  for y in range(26):
   if y==24 or y in cores[j]:continue
   G=cores[j]|{24,y}
   if F&G!={24}:continue
   matches=[]
   for name,RF,RG in reps:
    for swap in [False,True]:
     perm=certify(G if swap else F,F if swap else G,RF,RG)
     if perm is not None:matches.append((name,swap,perm))
   assert matches
   assert len({m[0] for m in matches})==1
   name,swap,perm=matches[0];counts[name]+=1;fcounts[ft]+=1
   records.append(dict(first_type=ft,G_owner=j,y=y,representative=name,swapped=swap,permutation=[perm[x] for x in range(26)]))
assert counts==dict(A_same=12,A_new=48,B=84) and fcounts=={0:64,1:80}
out=dict(representatives=[dict(name=n,F=sorted(f),G=sorted(g)) for n,f,g in reps],counts=dict(counts),first_type_counts=dict(fcounts),total=len(records),witnesses=records)
json.dump(out,open('workspace/agent4_private_two_external_pair_orbits.json','w'));open('workspace/agent4_private_two_external_pair_orbits.py','w').write(open(__file__).read());print(dict(counts),dict(fcounts),'total',len(records))
