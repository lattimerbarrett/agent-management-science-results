import json,itertools,numpy as np
N=1<<14

def flat_points(mask):
 p=[0]
 for i in range(14):
  if mask>>i&1:p +=[x^(1<<i) for x in p]
 return p

records=[]
for w,ms in json.load(open('workspace/agent4_flat_seeds.json')).items():
 records.append((int(w),ms,127,None))
records.append((362,[3373,13010,13665,9585,7213],127,(1,2,4)))
for w,r in json.load(open('workspace/a1_highresidue_seeds.json')).items():
 records.append((int(w),r['masks'],r['parallel_free'],None))
assert len(records)==64 and len({w%128 for w,_,_,_ in records})==64
coverage=set();summary=[]
for w,ms,U,shear in sorted(records):
 assert U.bit_count()==7 and all(m.bit_count()==7 for m in ms)
 flats=[flat_points(m) for m in ms]
 if shear:
  j,dst,src=shear
  flats[j]=[x^(((x>>src)&1)<<dst) for x in flats[j]]
 support=set()
 for p in flats:support.symmetric_difference_update(p)
 assert len(support)==w,(w,len(support))
 # Independent Boolean ANF transform, not just structural degree assertion.
 a=np.zeros(N,dtype=np.int8);a[list(support)]=1
 h=1
 while h<N:
  aa=a.reshape(-1,2*h);aa[:,h:] ^=aa[:,:h];h*=2
 assert max(int(m).bit_count() for m in np.flatnonzero(a))<=7
 quotient_mask=(N-1)^U
 occupied={x&quotient_mask for p in flats for x in p}
 missing=128-len(occupied)
 assert missing>=62,(w,missing)
 # Every missingcosetisadisjointaffine7flat, indicator degree7.
 newweights={w+128*k for k in range(missing+1)}
 coverage.update(newweights);coverage.update(N-v for v in newweights)
 summary.append({'weight':w,'parallel_free':U,'occupied':len(occupied),'missed':missing})
unknown={322,326,330,334};unknown.update(N-w for w in list(unknown))
expected=set(range(312,N-310,2))
assert expected-coverage==unknown,sorted(expected-coverage)
assert coverage<=expected
print('CHECKED',len(records),'seedwords; ANF degree<=7 and disjoint-coset counts independently verified.')
print('Covered',len(coverage),'of',len(expected),'central evenweights.')
print('Preciselyuncovered:',sorted(expected-coverage))
json.dump(summary,open('workspace/a1_central_seed_summary.json','w'),indent=2)
open('workspace/a1_central_all_but_four.py','w').write(open(__file__).read())
