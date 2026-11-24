import sympy as S
m,u,v,c,d,e,x=S.symbols('m u v c d e x',real=True)
# General centered symmetric nodes, B=(x²-c)/d in {+-1}.
M=[1,m,c+d*u,c*m+d*v,c*c+d*d+2*c*d*u,(c*c+d*d)*m+2*c*d*v,c*(c*c+3*d*d)+d*(3*c*c+d*d)*u,c*(c*c+3*d*d)*m+d*(3*c*c+d*d)*v]
def E(poly):
 return S.Poly(S.expand(poly),x).eval(0) if False else sum(co*M[po[0]] for po,co in S.Poly(poly,x).terms())
a=d*(m*u-v)/(c+d*u-m*m);b=-c-d*u-a*m
q=x*x+a*x+b
h=S.factor(E(q*q))
f=[S.factor(E(q*q*g)/h) for g in [x,(x*x-c)/d,x*(x*x-c)/d]]
# save exact expressions before Taylor
import pickle
with open('workspace/s2_symmap_agent2.pkl','wb') as fp:pickle.dump((m,u,v,c,d,f),fp)
# Multivariate Taylor via quotient polynomials in epsilon, degree2.
def jets(z):
 num,den=S.fraction(S.cancel(z))
 num=S.Poly(num.subs({u:u*e,v:v*e},simultaneous=True),e)
 den=S.Poly(den.subs({u:u*e,v:v*e},simultaneous=True),e)
 out=[]
 for k in range(4):
  out.append(S.factor((num.nth(k)-sum(den.nth(j)*out[k-j] for j in range(1,k+1)))/den.nth(0)))
 return out
jetsf=[jets(z) for z in f]
for a0 in jetsf:print('T',a0,flush=True)
# T2 Taylor via full-coordinate J and Hessian: delta=(0,u,v), first order L, second Q.
J=S.Matrix([[S.diff(z[1],u),S.diff(z[1],v)] for z in jetsf])
# f first order at m; tangent m is unchanged. Compose using expansions f(m+L0+Q0, L1+Q1,L2+Q2).
L=[z[1] for z in jetsf];Q=[z[2] for z in jetsf]
for i in range(3):
 quad=Q[i] if i==0 else 0
 quad+=sum(J[i,j]*Q[j+1] for j in range(2))
 quad+=S.diff(L[i],m).subs({u:L[1],v:L[2]},simultaneous=True)*L[0]
 quad+=Q[i].subs({u:L[1],v:L[2]},simultaneous=True)
 print('T2quad',i,S.factor(quad),flush=True)
 C=[z[3] for z in jetsf]
 sub={u:L[1],v:L[2]}
 cubic=C[i] if i==0 else 0
 cubic+=sum(J[i,j]*C[j+1] for j in range(2))
 cubic+=S.diff(L[i],m).subs({u:Q[1],v:Q[2]},simultaneous=True)*L[0]
 cubic+=S.diff(L[i],m).subs(sub,simultaneous=True)*Q[0]
 cubic+=S.diff(L[i],m,2).subs(sub,simultaneous=True)*L[0]**2/2
 cubic+=sum(S.diff(Q[i],z).subs(sub,simultaneous=True)*Q[j+1] for j,z in enumerate([u,v]))
 cubic+=S.diff(Q[i],m).subs(sub,simultaneous=True)*L[0]
 cubic+=C[i].subs(sub,simultaneous=True)
 print('T2cubic',i,S.factor(cubic),flush=True)
from pathlib import Path
Path('workspace/s2_normal_form_agent2.py').write_text(Path(__file__).read_text())
