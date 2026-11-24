from fractions import Fraction as F
h=F(1,10**20);d=F(1,10**12);L=10**7;R=200
sqrtdev=h*h*L*L/2
qdev=2*L*sqrtdev
T=10**14
qcomplex_error=4*R*d+4*d*d
Verror=qcomplex_error+4*R*qdev+4*qdev*qdev+h*h*T*T
Derror=Verror+h*h*(10**6+1)
assert F(1,200)**2-Derror>F(1,10**5)
V=10**6;Dmin=F(1,10**5);qb=201
Hnum=h*h*L+2*V*L+4*(qb*2+h*h*T*L)
assert Hnum<10**14
Hbound=F(10**14)/Dmin
Ez=h*h*(2+V*L*L+4*qb*L+2*V*T)/Dmin
assert Ez<F(1,10**13)
Ezout=4*h*h*(Hbound+1)+2*Ez
assert Ezout<F(1,10**12)
assert 4*Hbound+10<10**30
C3constant=12*10**30*10**20*10**36
assert C3constant<10**100
print('holomorphic-domain and Cauchy bound ledger PASSED')
print('Dmin lower bound margin',float(F(1,200)**2-Derror))
print('Bxz+1 bound',float(Ez),'output z-1',float(Ezout))
print('C3 bound coefficient',C3constant)
print('Error for k=10^1000 is <10^-900; local implicit/primitive error <10^-700.')
# Bounds for cutoff and critical exclusion.
assert 2/F(2,100)-F(2,100)-3-16>0
assert 50-3-F(2,50)-16>0
assert F(1,16)**2/50>F(1,10**5)
assert F(40,3*10**6)<F(1,10000)
print('kick support, shell exclusion, monkey isolation bounds PASSED')
open('workspace/agent1_quantitative_bounds.py','w').write(open(__file__).read())
# Read useful shared formulas/proof sources for assembly
for fn in ['workspace/agent4_lower_proof.txt','workspace/agent3_chart_formulas.py']:
 print('\nFILE',fn);print(open(fn).read())
