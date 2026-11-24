import itertools,json
terms=[{0:1,1:0},{1:1,2:0},{2:1,0:0}]
rows=[]
for x in itertools.product([0,1],repeat=3):
 hit=[i for i,t in enumerate(terms) if all(x[j]==v for j,v in t.items())]
 assert len(hit)==int(len(set(x))>1)
 rows.append(dict(x=x,satisfied=hit))
zero=(0,0,0)
for C in itertools.combinations(range(3),2):
 assert any(len(set(x))>1 and all(x[j]==0 for j in C) for x in itertools.product([0,1],repeat=3))
positive=[{j for j,v in t.items() if v} for t in terms]
support=[set(t) for t in terms]
def tau(H):
 for s in range(4):
  for C in itertools.combinations(range(3),s):
   if all(set(C)&e for e in H):return s
assert tau(positive)==3 and tau(support)==2
for j in range(3):
 for v in [0,1]:assert any(len(set(x))==1 and x[j]==v for x in itertools.product([0,1],repeat=3))
out=dict(truth=rows,positive_cover=tau(positive),support_cover=tau(support),C0_at_zero=3,UC1=2)
json.dump(out,open('workspace/agent4_nae3_support_obstruction.json','w'));open('workspace/agent4_nae3_support_obstruction.py','w').write(open(__file__).read());print(out)
