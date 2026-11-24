import sympy as s
E=s.symbols('e', integer=True, nonnegative=True)
def dot(D,F):
 a,b=D;c,d=F;return s.expand(-E*a*c+a*d+b*c)
A=(5,-1);B=(-1,12*E+5);H=(1,3*E+1);P=(4,12*E+3);K=(-2,-E-2);C=(4,12*E+4)
chi=s.simplify(2+(dot(C,C)-dot(C,K))/2-dot(A,B))
print('c1sq,c2,chi',dot(C,C),dot(A,B),chi)
print('slopes',dot(A,P),dot(B,P),dot(C,P)/2)
def h0(a,b,e):
 return sum(max(b-i*e+1,0) for i in range(a+1)) if a>=0 else 0
def coh(a,b,e):
 z=h0(a,b,e);t=h0(-2-a,-e-2-b,e)
 chi=1+((-e*a*a+2*a*b)-((e-2)*a-2*b))//2
 return z,z+t-chi,t
for e in range(6):
 print('e',e,'A',coh(5,-1,e),'B',coh(-1,12*e+5,e),'A-B',coh(6,-12*e-6,e),'B-A',coh(-6,12*e+6,e))
assert chi == -15*E
assert dot(A,P)==40*E+11 and dot(B,P)==40*E+17
assert dot(A,B)==65*E+26
# Exact symbolic cohomology sums; no finite sampling is used here.
i=s.symbols('i', integer=True, nonnegative=True)
assert s.summation(i*E,(i,0,5))==15*E
assert s.summation(12*E+5+i*E,(i,0,6))==105*E+35
def rr(a,b):
 return s.expand(1+(-E*a*a+2*a*b-(E-2)*a+2*b)/2)
assert -rr(-6,12*E+6)==75*E+35
assert rr(-1,12*E+5)==0
print('All symbolic intersection/RR/cohomology identities passed.')
with open('workspace/agent2_cohomology.py','w') as f:
 f.write('''def h0(a,b,e):
    return sum(max(b-i*e+1,0) for i in range(a+1)) if a>=0 else 0

def cohomology(a,b,e):
    h_0=h0(a,b,e)
    h_2=h0(-2-a,-e-2-b,e)
    chi=1+(-e*a*a+2*a*b-(e-2)*a+2*b)//2
    return h_0,h_0+h_2-chi,h_2
''')