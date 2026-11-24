import itertools,json,time
st=time.time();records=[]
for t,startc in [(3,3),(5,5)]:
 cores=[set(range(i*startc,(i+1)*startc)) for i in range(t)];patterns=[{tuple(j for j in range(t) if 1<=(j-i)%t<=(t-1)//2)} for i in range(t)]
 locked=set();stages=[];tested=0
 def members(cs):
  H=[]
  for i,ts in enumerate(patterns):
   for T in ts:
    for choice in itertools.product(*[sorted(cs[j]) for j in T]):H.append((i,sum(1<<x for x in cs[i]|set(choice))))
  return H
 def covers_of_size(cs,s):
  global tested
  V=sorted(set.union(*cs));H=members(cs);cov=[]
  for C in itertools.combinations(V,s):
   tested+=1;m=sum(1<<x for x in C)
   if all(m&F for _,F in H):cov.append(m)
  return cov
 for i in range(t):
  while True:
   H=members(cores)
   assert all(F&G for _,F in H for _,G in H)
   assert not covers_of_size(cores,t-1)
   C=covers_of_size(cores,t)
   assert C
   masks=[sum(1<<x for x in cs) for cs in cores]
   for m in C:
    for mask in masks:
     meet=(mask&m).bit_count()
     assert meet==mask.bit_count() or meet<=1
   good=[m for m in C if m&masks[i]==masks[i]]
   if good:
    a,b=sorted(cores[i])[:2];forbidden=[set(cs) for cs in cores];forbidden[i].remove(b)
    assert covers_of_size(forbidden,t-1)
    m=good[0];T=tuple(j for j in range(t) if j!=i and m&masks[j]);assert len(cores[i])+len(T)==t
    oldH={F for _,F in H};patterns[i].add(T);new=members(cores)
    assert all(F.bit_count()==t for j,F in new if j==i and any(F==sum(1<<x for x in cores[i]|set(ch)) for ch in itertools.product(*[sorted(cores[j]) for j in T])))
    assert all(F&G for _,F in new for _,G in new)
    locked.add(i);stages.append(dict(action='lock',i=i,core_sizes=list(map(len,cores)),T=T,mincovers=len(C)));break
   a,b=sorted(cores[i])[:2];oldpair=any(m>>a&1 and m>>b&1 for m in C);assert not oldpair
   merged=[set(cs) for cs in cores];merged[i].remove(b)
   # In all-choice form removing b is exactly the same-core quotient b->a.
   newbad=covers_of_size(merged,t-1);assert bool(newbad)==oldpair
   cores=merged;stages.append(dict(action='merge',i=i,removed=b,core_sizes=list(map(len,cores))))
   for j in locked:
    assert all(F.bit_count()==t for jj,F in members(cores) if jj==j)
 assert list(map(len,cores))==[(t+1)//2]*t
 records.append(dict(t=t,start_core=startc,end_core_sizes=list(map(len,cores)),tested_cover_candidates=tested,stages=stages))
 print('checked',t,tested,len(stages),flush=True)
out=dict(records=records,seconds=time.time()-st)
json.dump(out,open('workspace/agent4_allchoice_lock_independent_check.json','w'));open('workspace/agent4_allchoice_lock_independent_check.py','w').write(open(__file__).read());print('seconds',out['seconds'])
