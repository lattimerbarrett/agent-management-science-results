"""Exact interval certificate for a FORMAL shape-energy minimum in n=19.
This checks finite-dimensional algebra ONLY. No PDE existence follows here.
"""
import sympy as S
import runpy,json
from pathlib import Path
base=runpy.run_path('workspace/agent3_exact_scale_signature.py')
j,n,D,x=[base[v] for v in ['j','n','D','x']]
Qs=base['Qs']; z=S.symbols('z'); dim=19
const=S.simplify(4*S.pi*S.gamma(S.Rational(dim+1,2))**2/S.gamma(S.Rational(dim+2,2))**2)
M=[S.expand((dim-1)**2*Q.subs({n:dim,j:0})*x+dim**2*Q.subs({n:dim,j:1})*const) for Q in Qs]
def moment(p):
    return S.expand(sum(c*M[mon[0]] for mon,c in S.Poly(p,D).terms()))
a=S.Rational(dim+1,2)
r2=[];r3=[];r1=[]
for k in range(4):
    r2k=0;r3k=0;r1k=0
    for m in range(k+1):
        numerator=S.prod(D+r*(dim-r) for r in range(m))
        den=S.prod(a-r for r in range(1,m+1))
        factor=(-1)**(k-m)*S.binomial(k,m)
        r2k+=factor*numerator/(S.factorial(m)*den)
        r3k+=factor*numerator/(S.factorial(m+1)*den)
        if m:
            num1=S.prod(D+(r+1)*(dim-1-r) for r in range(m-1))
            den1=S.factorial(m-1)*S.prod(S.Rational(dim-1,2)-r for r in range(1,m))
            r1k+=2*factor*num1/den1
    r2.append(S.expand(r2k));r3.append(S.expand(r3k));r1.append(S.expand(r1k))
G2=S.Matrix(4,4,lambda k,l:moment(r2[k]*r2[l]))
assert G2==base['make_gram'](19)
G1=S.Matrix(4,4,lambda k,l:moment(D*r1[k]*r1[l]/(dim-1)**2))
G3=S.Matrix(3,3,lambda k,l:moment((D-dim-1)*r3[k]*r3[l]))
dd=dim-1; rho=S.Rational(1,dd)
B=S.zeros(4)
for k in range(4):
    for l in range(4):
        ck=1+S.Rational(2*k,dd+2);cl=1+S.Rational(2*l,dd+2)
        B[k,l]=2*(dd+2)*rho*ck*cl*G1[k,l]
        if k and l:
            B[k,l]+=4*(S.Rational(1,dd+4)+2*dd*rho/((dd+2)*(dd+4)))*k*l*G3[k-1,l-1]
        if l:
            B[k,l]+=l*(2+8*rho+4*(1+4*rho)*(l-1)/(dd+4))*G2[k,l-1]
B=(B+B.T)/2
coef=[S.Integer(1),-S.Rational(41747268,10**8),S.Rational(4639947,10**8),-S.Rational(105709,10**8)]
P=S.expand(sum((k+l+1)*G2[k,l]*coef[k]*coef[l]*z**(k+l) for k in range(4) for l in range(4)))
T=S.expand(sum(B[k,l]*coef[k]*coef[l]*z**(k+l) for k in range(4) for l in range(4)))
xlo,xhi=base['xlo'],base['xhi']
def enclosure(poly,zlo,zhi):
    low=0;up=0
    for (i,k),c in S.Poly(poly,x,z).terms():
        left=xlo**i*zlo**k;right=xhi**i*zhi**k
        if c>=0:low+=c*left;up+=c*right
        else:low+=c*right;up+=c*left
    return low,up

def sign_at(poly,value):
    low,up=enclosure(poly,value,value)
    return 1 if low>0 else (-1 if up<0 else 0)
lo=S.Rational(999,1000);hi=S.Rational(1001,1000)
assert sign_at(P,lo)==1 and sign_at(P,hi)==-1
for _ in range(45):
    mid=(lo+hi)/2;sgn=sign_at(P,mid)
    assert sgn
    if sgn>0:lo=mid
    else:hi=mid
assert enclosure(S.diff(P,z),lo,hi)[1]<0
assert enclosure(T,lo,hi)[1]<0
print('Certified root interval for lambda^2:',float(lo),float(hi))
print('P(left)>0>P(right); P derivative strictly negative throughout root interval.')
print('Full balanced translation bracket strictly negative throughout root interval.')
print('Thus the FORMAL negative-DN shape model has a strict full local minimum in n=19.')
print('This is NOT a PDE counterexample or a gluing theorem.')
Path('workspace/agent3_n19_formal_certificate.json').write_text(json.dumps({'lambda_squared_lower':str(lo),'lambda_squared_upper':str(hi),'polynomial_coefficients':[str(v) for v in coef],'P':str(P),'translation_bracket':str(T)}))
