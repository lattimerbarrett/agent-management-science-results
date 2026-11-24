import sympy as S,pickle
from pathlib import Path
m,h,z,s,d,a,b,H,out=pickle.load(open('workspace/s2_twonegat_map_agent2.pkl','rb'))
e=S.symbols('e')
def jets(expr):
 num,den=S.fraction(S.cancel(expr));su={h:e*h,z:e*z,s:e*e*s,d:e*e*d}
 num=S.Poly(num.subs(su,simultaneous=True),e);den=S.Poly(den.subs(su,simultaneous=True),e)
 ans=[]
 for k in range(4):ans.append(S.factor((num.nth(k)-sum(den.nth(j)*ans[k-j] for j in range(1,k+1)))/den.nth(0)))
 return ans
F=[jets(fo.subs({a:1,b:4,H:2})) for fo in out]
G=[jets(fo.subs({a:4,b:1,H:2})) for fo in out]
L=[row[1] for row in F];Q=[row[2] for row in F];C=[row[3] for row in F]
print('F L',L,flush=True)
sub={h:L[1],z:L[2],s:Q[3],d:Q[4]}
res=[]
for i in range(5):
 one=(L[0] if i==0 else 0)+G[i][1].subs(sub,simultaneous=True)
 two=(Q[0] if i==0 else 0)+sum(S.diff(G[i][1],zz).subs(sub,simultaneous=True)*Q[j] for j,zz in [(1,h),(2,z)])+S.diff(G[i][1],m).subs(sub,simultaneous=True)*L[0]+G[i][2].subs(sub,simultaneous=True)
 three=None
 if i>=3:
  three=sum(S.diff(G[i][2],zz).subs(sub,simultaneous=True)*C[j] for j,zz in [(3,s),(4,d)])+S.diff(G[i][2],m).subs(sub,simultaneous=True)*L[0]+G[i][3].subs(sub,simultaneous=True)
 one,two=S.factor(one),S.factor(two)
 if three is not None:three=S.factor(three)
 res.append([one,two,three]);print('RESULT',i,res[-1],flush=True)
pickle.dump((m,h,z,s,d,res),open('workspace/s2_two_neutral_nf_agent2.pkl','wb'))
Path('workspace/s2_two_neutral_nf_agent2.py').write_text(Path(__file__).read_text())
