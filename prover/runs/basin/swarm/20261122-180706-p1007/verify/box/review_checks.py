from pathlib import Path
exec(Path('agents/agent_1/scratchpad.py').read_text())

# Check all, rather than just middle-block, modification conditions and
# transversality for both filtrations in rank 4.
import sympy as s
z,t,lam=s.symbols('z t lam')
n=4
R=s.zeros(n); R[1,1]=lam; R[2,1]=lam*t
M=s.zeros(n)
for i in range(n):
    for j in range(n):
        if i<=j+1:
            M[i,j]=s.Symbol(f'a{i+1}{j+1}')+z*s.Symbol(f'b{i+1}{j+1}')
M[3,2]=z*s.Symbol('b43')
M[0,1]=-t*s.Symbol('a13')+z*s.Symbol('b12')
M[2,1]=t*s.Symbol('a22')+t*t*s.Symbol('a23')-t*s.Symbol('a33')+z*s.Symbol('b32')
A=R/z+M
G=s.eye(n); G[1,1]=1/z; G[2,1]=t/z
An=s.simplify(G.inv()*A*G+lam*G.inv()*G.diff(z))
assert all(s.simplify(s.limit(z*x,z,0))==0 for x in An)
A0=An.subs(t,0)
assert all(s.simplify(A0[i,j])==0 for i in range(n) for j in range(n) if i>j+1)
H=s.eye(n); H[1:3,1:3]=s.Matrix([[z,1],[-t,0]])
Ap=s.simplify(H.inv()*An*H+lam*H.inv()*H.diff(z))
assert all(s.simplify(Ap[i,j])==0 for i in range(n) for j in range(n) if i>j+1)
assert all(s.simplify(s.limit(z*x,z,0))==0 for x in Ap)
print('Full 4-by-4 modification/regularity/transversality checks passed.')
print('generic middle graded arrow:',s.factor(Ap[2,1]))
