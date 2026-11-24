import sys,json
sys.path.insert(0,'workspace')
import sympy as s
from agent2_p3_chern_constraints import constraints
from agent1_chern_eliminate import eliminate

def check():
 out=[]
 for r in range(2,6):
  for l in range(1,r):
   k=r-l
   E,V,S0=constraints((l,k),(0,1));E,V,S=eliminate(E,V);subs=S0|S
   if V:
    weights=[int(str(v)[-2])+int(str(v)[-1]) for v in V]
    def order(m):return (sum(w*a for w,a in zip(weights,m)),tuple(-a for a in m[::-1]))
    G=s.groebner(E,*V,order=order,domain=s.QQ)
    points=s.solve(list(G),V)
    if isinstance(points,dict):points=[tuple(points[v] for v in V)]
   else:points=[()];assert all(e==0 for e in E)
   classes=[]
   for p in points:
    D=dict(zip(V,p))
    for it in range(20):
     D.update({v:s.expand(val.subs(D)) for v,val in subs.items()})
    a=D.get(s.Symbol('c0_10'),0)
    b=D.get(s.Symbol('c0_20'),0)
    assert a in (0,1) and b in (0,1)
    assert (a,b) in ((0,0),(1,0),(1,1))
    assert l>=2 or b==0
    classes.append((int(a),int(b)))
   out.append({'rank':r,'low':l,'high':k,'low_fiber_c1c2':sorted(set(classes))})
 print(json.dumps(out,indent=2))
 with open('workspace/agent2_p3_1uniform_table.json','w') as f:json.dump(out,f,indent=2)
 return out
if __name__=='__main__':
 check()
