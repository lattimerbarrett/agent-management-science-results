import json
import sympy as S
from itertools import combinations

def inv(w):return tuple(-x for x in w[::-1])
def cat(*ws):
 out=[]
 for w in ws:
  for x in w:
   if out and out[-1]==-x:out.pop()
   else:out.append(x)
 return tuple(out)
def cm(a,b):return cat(a,b,inv(a),inv(b))
def fox(word,ts):
 # Fox derivative evaluated at commutative character xi->ts[i].
 ans=[0]*len(ts);p=1
 for x in word:
  i=abs(x)-1
  if x>0:ans[i]+=p;p*=ts[i]
  else:p//=ts[i];ans[i]-=p
 return ans
X=[(1,),(2,),(3,)];gens=[];names=[]
for i in range(3):
 for j in range(3):
  if i!=j:
   A=X.copy();A[i]=cat(X[j],X[i],inv(X[j]));gens.append(A);names.append(('C',i+1,j+1))
for i in range(3):
 j,k=[a for a in range(3) if a!=i];A=X.copy();A[i]=cat(cm(X[j],X[k]),X[i]);gens.append(A);names.append(('M',i+1,j+1,k+1))
ts=[1,-1,1];mat=[]
for name,A in zip(names,gens):
 J=S.Matrix([fox(w,ts) for w in A])
 assert J*S.Matrix([0,-2,0])==S.Matrix([0,-2,0])
 assert J[0,1]==J[2,1]==0
 block=J.extract([0,2],[0,2]).T
 mat.append(block);print(name,block.tolist())
D=S.diag(-1,1);N=-S.eye(2);U=mat[6];V=mat[8]
expected=[D,S.eye(2),S.eye(2),S.eye(2),S.eye(2),N*D,U,S.eye(2),V]
assert mat==expected
assert D*U*D==U.inv() and D*V*D==V.inv()
assert U.det()==V.det()==1
# Quotient free-product representation UT4(F2).
def mul(A,B):return (A*B).applyfunc(lambda x:x%2)
def invert(A):return A.inv().applyfunc(lambda x:x%2)
I=S.eye(4);a=I.copy();a[0,1]=1;b=I.copy();b[1,2]=1;c=I.copy();c[2,3]=1
d=a;u=mul(b,a);v=mul(c,a)
assert mul(d,d)==I and mul(mul(mul(d,u),d),u)==I and mul(mul(mul(d,v),d),v)==I
images=[d,I,I,I,I,d,u,I,v]
candidate=json.load(open('workspace/agent3_cubic_candidates.json'))['candidates'][0]['word']
R=I
for x in candidate:R=mul(R,images[x-1] if x>0 else invert(images[-x-1]))
assert R!=I
print('candidate image UT4(F2)',R.tolist())
assert R==I+S.eye(4)[:,0]*S.eye(4)[3,:]
# Independently exact Johnson degree3 zero using associative derivations.
from agent1_integral_derivations import bracket
G=[]
for name in names:
 if name[0]=='C':_,i,j=name;G.append({(i-1,(j-1,i-1)):1,(i-1,(i-1,j-1)):-1})
 else:_,i,j,k=name;G.append({(i-1,(j-1,k-1)):1,(i-1,(k-1,j-1)):-1})
J1=bracket(bracket(G[8],G[0]),G[6]);J2=bracket(bracket(G[6],G[0]),G[8])
assert J1==J2
print('exact Johnson3 cancellation verified',len(J1))
