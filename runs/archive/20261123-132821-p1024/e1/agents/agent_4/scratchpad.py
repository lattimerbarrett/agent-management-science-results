import sys,json
sys.path.insert(0,'workspace')
from agent4_cech import compute
out=[]
for g in range(2,13):
 r=(g+2)//3;N=2*g-2
 vectors=[[int(i==j) for i in range(r)] for j in range(r)]
 vectors += [[1]*r,[(-1)**j*(j+1) for j in range(r)]]
 for b in vectors:
  vals=[compute(g,b,a,d) for a,d in [(0,0),(1,0),(0,-N),(1,-N)]]
  delta=vals[0]+vals[3]-vals[1]-vals[2]
  expected=-max(j for j,c in enumerate(b) if c)
  assert delta==expected,(g,b,vals,delta,expected)
  out.append(dict(g=g,b=b,dimensions=vals,delta=delta))
 print('verified g=',g,'vectors=',len(vectors),flush=True)
 with open('workspace/agent4_general_checks.json','w') as f:json.dump(out,f)
print('total',len(out))
