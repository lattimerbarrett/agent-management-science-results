import math,itertools,networkx as nx,sys,json
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,'workspace');from agent2_cycles import brute
TRI={(0,0):1,(1,1):3,(2,1):3};STAR5={(0,0):1,(1,1):5,(2,1):10};EMPTY={(0,0):1}
def count(a,b,optsA,optsB,ic=0):
 fac=[math.factorial(i) for i in range(max(a,b)+1)];ans=F(ic)
 for (ja,pa),va in optsA.items():
  for (jb,pb),vb in optsB.items():
   for k in range(max(1,pa,pb),min(a-ja,b-jb)+1):
    if ja+jb==0 and k==1:continue
    if not 0<=k-pa<=a-ja-pa or not 0<=k-pb<=b-jb-pb:continue
    ans+=F(va*vb*math.comb(a-ja-pa,k-pa)*math.comb(b-jb-pb,k-pb)*2**(pa+pb)*fac[k]*fac[k-1],2)
 assert ans.denominator==1;return ans.numerator
for a,b,oa,ob,fa,fb,ic in [(3,3,TRI,TRI,nx.complete_graph(3),nx.complete_graph(3),2),(1,6,EMPTY,STAR5,nx.empty_graph(1),nx.star_graph(5),0)]:
 E=list(nx.complete_bipartite_graph(a,b).edges())+list(fa.edges())+[(x+a,y+a) for x,y in fb.edges()]
 assert count(a,b,oa,ob,ic)==brute(a+b,E)
rows=[]
for m in [5,6,8,10,20,40,80,160,320]:
 ed=count(m,m+1,TRI,TRI,2);alt=count(m,m+1,EMPTY,STAR5)
 if m>=40:assert alt>ed
 rows.append({'n':2*m+1,'ratio':float(F(alt,ed)),'m_times_ratio_minus1':float(m*F(alt-ed,ed))})
print(rows)
# Exact Bessel inequality: betaA=2I2/I1<2, betaB=betaA+2;
# star5 advantage =2betaB-3betaA=4-betaA>2.
for s in range(50):assert math.factorial(s+2)>math.factorial(s+1)
Path('workspace/agent2_H17_odd_cycles.json').write_text(json.dumps(rows,indent=2))
Path('workspace/agent2_H17_odd_cycles.py').write_text(Path(__file__).read_text())
