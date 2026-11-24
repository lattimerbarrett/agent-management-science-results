import sympy as s,json
U=s.Matrix([[1,2],[0,1]]);V=s.Matrix([[1,0],[2,1]]);R=s.diag(-1,1);Z=-s.eye(2)
# row-Jacobian, character all -1, quotient fixedline coordinates x1-x3,x2-x3
names=[];mats=[]
for i in range(3):
 for j in range(3):
  if i==j:continue
  A=s.eye(3);A[i,i]=-1;A[i,j]=2
  Q=s.Matrix([[A[0,0]-A[2,0],A[0,1]-A[2,1]],[A[1,0]-A[2,0],A[1,1]-A[2,1]]])
  names.append(f'K{i+1}{j+1}');mats.append(Q)
 js=[j for j in range(3) if j!=i];j,k=js
 A=s.eye(3);A[i,j]=2;A[i,k]=-2
 Q=s.Matrix([[A[0,0]-A[2,0],A[0,1]-A[2,1]],[A[1,0]-A[2,0],A[1,1]-A[2,1]]])
 names.append(f'C{i+1};{j+1}{k+1}');mats.append(Q)
expected=[U*R,R,U,Z*V*R,Z*R,V,V*R,Z*U*R,Z*V*U**-1]
assert mats==expected
assert R*U*R==U**-1 and R*V*R==V**-1
for a,b in zip(names,mats):print(a,b.tolist())
# affine quotient U=a=(−1,0), V=b=(−1,1), R=Z=identity
A=(-1,0);B=(-1,1);Id=(1,0)
def mul(a,b):return(a[0]*b[0],a[1]+a[0]*b[1])
def inv(a):return(a[0],-a[0]*a[1])
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
# Invert row matrices to turn the Fox anti-homomorphism into a homomorphism.
G=[A,Id,A,B,Id,B,B,A,mul(A,B)]
w=comm(G[0],comm(G[2],G[8]));print('base affine',w)
assert w==(1,-4)
for c in range(3,12):
 assert w[0]==1 and abs(w[1])==2**(c-1)
 w=comm(A,w)
print('iterated affine formulas verified through c=11')
open('workspace/agent3_n3_checks.py','w').write(open(__file__).read())
