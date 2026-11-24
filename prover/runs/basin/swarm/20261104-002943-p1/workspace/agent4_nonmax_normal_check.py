import sympy as S,pickle
from pathlib import Path
x=list(map(S.Integer,[-8,-7,-4,-1,1,4,7,8]));V=S.Matrix([[a**j for j in range(4)] for a in x]);r=S.Rational(591,13);ss=S.Rational(711,13);delta=(r*r-2529)/4
q=S.Matrix([(a*a-(65+r)/2)*(a*a-(65-ss)/2) for a in x]);Q=S.Matrix([(a*a-(65-r)/2)*(a*a-(65+ss)/2) for a in x]);C=360**2-delta**2
assert all(q[i]*Q[i]==C for i in range(8))
Cons=S.ones(1,8).col_join(V.T*S.diag(*q));rhs=S.Matrix([1,0,0,0,0]);w0=S.ones(8,1)/8;w0=w0+Cons.T*(Cons*Cons.T).inv()*(rhs-Cons*w0)
assert min(w0)>0
hvars=S.symbols('h0:4');h=V*S.Matrix(hvars);u=S.matrix_multiply_elementwise(S.matrix_multiply_elementwise(w0,q),h)
def smul(a,b):return S.matrix_multiply_elementwise(a,b)
def expand(M):return M.applyfunc(S.expand)
def step(w):
 N=len(w);M=[V.T*S.diag(*a)*V for a in w];cc=[V.T*smul(S.Matrix([a**4 for a in x]),a) for a in w];MI=M[0].inv();aa=[]
 for k in range(N):aa.append(expand(MI*(cc[k]-sum((M[j]*aa[k-j] for j in range(1,k+1)),S.zeros(4,1)))))
 p=[S.Matrix([a**4 for a in x])-V*aa[0]]+[-V*aa[j] for j in range(1,N)]
 pp=[expand(sum((smul(p[j],p[k-j]) for j in range(k+1)),S.zeros(8,1))) for k in range(N)]
 num=[expand(sum((smul(w[j],pp[k-j]) for j in range(k+1)),S.zeros(8,1))) for k in range(N)];den=[sum(a) for a in num];out=[]
 for k in range(N):out.append(expand((num[k]-sum((out[k-j]*den[j] for j in range(1,k+1)),S.zeros(8,1)))/den[0]))
 return out
f2=step(step([w0,u,S.zeros(8,1)]));b1=expand(f2[1]-u)
assert f2[0]==w0 and V.T*smul(q,b1)==S.zeros(4,1)
# c=V.T diag(q)w, normal frame u=w q h. G=V.T diag(w q²)V
G=V.T*S.diag(*smul(w0,smul(q,q)))*V
c2=V.T*smul(q,f2[2]);Gb=V.T*S.diag(*smul(b1,smul(q,q)))*V
hflow=expand(G.inv()*(c2-Gb*S.Matrix(hvars)))
res=dict(x=x,V=V,q=q,Q=Q,C=C,w0=w0,hvars=hvars,u=u,b1=b1,f2=f2,hflow=hflow)
with open('workspace/agent4_nonmax_normal_jet.pkl','wb') as f:pickle.dump(res,f)
print('w0=',w0.T,'C=',C)
print('hflow=')
for a in hflow:print(S.factor(a))
L=26*hvars[0]+965*hvars[2]; O=12545*hvars[1]+675713*hvars[3]
Ld=S.factor(26*hflow[0]+965*hflow[2]);Od=S.factor(12545*hflow[1]+675713*hflow[3]);print('Ld',Ld);print('Od',Od)
# invariant odd combination
rat=S.factor(hflow[1]/hflow[3]);print('odd flow ratio',rat)
I=hvars[1]-rat*hvars[3];lv,ov,iv=S.symbols('L O I');sol=S.solve([L-lv,O-ov,I-iv], [hvars[0],hvars[1],hvars[3]])
print('Ld transformed',S.factor(Ld.subs(sol)));print('Od transformed',S.factor(Od.subs(sol)))
fld=S.factor(Ld.subs(sol));pol=S.Poly(fld.subs({lv:0,iv:1}),ov)
print('discriminant sign',S.sign(S.discriminant(pol.as_expr(),ov)));print('O eq roots',S.nroots(pol))
print('approx transformed field',S.Poly(fld,lv,ov,iv).terms().__repr__()[:100]);print([float(a) for a in S.Poly(fld,lv,ov,iv).coeffs()])
print('saved all exact expressions')
