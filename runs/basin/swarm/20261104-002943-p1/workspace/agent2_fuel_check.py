import pickle,sympy as S
D=pickle.load(open('workspace/agent4_nonmax_normal_jet.pkl','rb'))
w,p,C,V,b,hvar,hflow=[D[k] for k in ['w0','q','C','V','b1','hvars','hflow']]
h=V*S.Matrix(hvar);dh=V*hflow
Fdot=sum(b[i]*p[i]**3*h[i]+w[i]*p[i]**3*dh[i] for i in range(8))
metric=sum((C+p[i]**2)*b[i]**2/w[i] for i in range(8))/4
assert S.expand(Fdot-metric)==0
print('Exact generic quartic-normal fuel identity verified for rational nonmaximal cycle.')
