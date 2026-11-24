import sympy as S
from pathlib import Path
x=list(map(S.Integer,[-8,-7,-4,-1,1,4,7,8])); n=8;s=4
V=S.Matrix([[a**j for j in range(s)] for a in x]);sigma=S.Matrix([1,-1,-1,1,1,-1,-1,1]);w0=S.ones(8,1)/8
hvars=S.symbols('h0:4'); h=V*S.Matrix(hvars)
u=S.matrix_multiply_elementwise(S.matrix_multiply_elementwise(w0,sigma),h)
def expmat(M):return M.applyfunc(S.expand)
def smul(a,b):return S.matrix_multiply_elementwise(a,b)
def step(w):
    N=len(w);M=[V.T*S.diag(*a)*V for a in w]; c=[V.T*smul(sigma,a) for a in w];MI=M[0].inv()
    aa=[]
    for k in range(N):aa.append(expmat(MI*(c[k]-sum((M[j]*aa[k-j] for j in range(1,k+1)),S.zeros(s,1)))))
    q=[sigma-V*aa[0]]+[-V*aa[j] for j in range(1,N)]
    qq=[expmat(sum((smul(q[j],q[k-j]) for j in range(k+1)),S.zeros(n,1))) for k in range(N)]
    numerator=[expmat(sum((smul(w[j],qq[k-j]) for j in range(k+1)),S.zeros(n,1))) for k in range(N)]
    den=[sum(a) for a in numerator];out=[]
    for k in range(N):out.append(expmat((numerator[k]-sum((out[k-j]*den[j] for j in range(1,k+1)),S.zeros(n,1)))/den[0]))
    return out
f1=step([w0,u,S.zeros(n,1),S.zeros(n,1)]);print('step1',flush=True)
f2=step(f1);print('step2',flush=True)
assert f2[0]==w0 and f2[1]==u
assert V.T*smul(sigma,f2[2])==S.zeros(s,1)
# changing normal projection h via c and M after two steps: c=t M0 h+t^3 c3; M=M0+t M(u)+t²M(f22)
# h_eff/t = h +t ( ... initial differs normal pure path ) ... record raw
out={'nodes':x,'V':V,'sigma':sigma,'w0':w0,'hvars':hvars,'u':u,'f2':f2}
import pickle
with open('workspace/agent4_rational_max_jet.pkl','wb') as f:pickle.dump(out,f)
print('saved jets; tangent quadratic:')
for a in f2[2]:print(S.factor(a))
print('normal cubic moment:')
for a in V.T*smul(sigma,f2[3]):print(S.factor(a))
