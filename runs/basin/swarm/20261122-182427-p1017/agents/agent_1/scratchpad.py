import itertools as it
import sympy as sp

q = sp.symbols('q')
m = (q**2 + 1)/2
N = q**4 + m
L = q**3*(q**3 + q**2 + q + 1)
B = m*q**4 + m*(m-1)/2
G = (q**2+1)*(q**2+q+1)
P = q**2*(G-m*(q**2+1))
A = q**2*m*(q**2+1)
T = m*(m-1)*q**4/2 + m*(m-1)*(m-2)/6
# (number of flats, points per flat, q-point lines, 2-point lines)
types = [(P,q**2,q*(q+1),0),
         (A,q**2+1,q*(q+1),q**2), (T,3,0,3)]
f = {():sp.Integer(1), (1,):N, (2,):L+B,
     (3,):P+A+T, (1,2):q*L+2*B,
     (1,3):sum(c*n for c,n,l,b in types),
     (2,3):sum(c*(l+b) for c,n,l,b in types),
     (1,2,3):sum(c*(q*l+2*b) for c,n,l,b in types)}
f = {S:sp.expand(v) for S,v in f.items()}
def flag(seq):
    return f[tuple(sorted(set(seq)-{0,4}))]
stable = [S for k in range(4) for S in it.combinations(range(2,7),k)
          if all(b-a>1 for a,b in zip(S,S[1:]))]
assert len(stable) == 13
alpha = {():sp.Integer(1)}
for S in stable[1:]:
    seqs = list(it.combinations_with_replacement(range(5),len(S)))
    terms = []
    for r1 in seqs:
        for r2 in seqs:
            b = tuple(k-i-j for k,i,j in zip(S,r1,r2))
            if all(x in (0,1) for x in b) and list(b)==sorted(b):
                terms.append(flag(r1)*flag(r2))
    alpha[S] = sp.expand(sum(terms))
beta = {S:sp.expand(sum((-1)**(len(S)-k)*alpha[U]
        for k in range(len(S)+1) for U in it.combinations(S,k)))
        for S in stable}
g = [sp.expand(sum(beta[S] for S in stable if len(S)==k)) for k in range(4)]
assert g[0] == 1
u,v,w,x = (f[S] for S in [(1,),(2,),(3,),(1,2)])
r,h = f[1,3]+f[2,3], f[1,2,3]
assert sp.expand(r-(P*(2*q**2+q)+A*(3*q**2+q+1)+6*T)) == 0
assert sp.expand(h-(P*(q**3+q**2)+A*(q**3+3*q**2)+6*T)) == 0
g1 = 2*u**2+4*u*v+4*u*w+6*u+2*v**2+4*v*w+6*v+w**2+4*w-1
g2 = (3*u**2+10*u*v+4*u*w-10*u+6*v**2+4*v*w-6*v-w**2-6*w-2
      +6*x*(u+v+w)+8*r*(u+v)+2*w*r+3*x**2+6*x*r+r**2+2*r)
g3 = (h**2+6*h*x-3*u**2-2*u*w-2*u*x+2*u*r+v**2-2*v*w+2*v*r-2*v
      +w**2-6*w*x-2*w*r+2*w+x**2+6*x*r+r**2-2*r+1)
for actual,formula in zip(g[1:],[g1,g2,g3]):
    assert sp.expand(actual-formula)==0

t,z = sp.symbols('t z')
H = sp.Poly(sum(g[k]*t**k*(1+t)**(6-2*k) for k in range(4)),t)
a = [H.nth(k) for k in range(7)]
expected = [1,6+g[1],15+4*g[1]+g[2],20+6*g[1]+2*g[2]+g[3]]
expected += expected[-2::-1]
assert all(sp.expand(b-c)==0 for b,c in zip(a,expected))
F = z**3+g[1]*z**2+g[2]*z+g[3]
assert sp.cancel(H.as_expr()-t**3*F.subs(z,(1+t)**2/t))==0
D = sp.Poly(sp.discriminant(F,z),q)
Cs = [sp.Poly(sp.expand(a[i]**2-a[i-1]*a[i+1]),q) for i in range(1,4)]
assert sp.expand(Cs[2].as_expr()-(a[3]-a[2])*(a[3]+a[2]))==0
# Exact sign certificates: index j is the exponent in P(q+3).
def shifted_signs(poly):
    poly = sp.Poly(poly,q).shift(3)
    return [int(sp.sign(poly.nth(j))) for j in range(poly.degree()+1)]
for k,degree in [(1,16),(2,16),(3,18)]:
    assert shifted_signs(g[k]) == [1]*(degree+1)
assert shifted_signs(Cs[0]) == [1]*33
assert shifted_signs(D) == [1]*61+[-1]*6
assert shifted_signs(Cs[1]) == [1]*33+[-1]*2
assert D.eval(44)>0 and D.eval(45)<0
assert Cs[1].eval(90)>0 and Cs[1].eval(91)<0
assert sp.factorint(45)=={3:2,5:1}
for n in (91,93,95):
    assert len(sp.factorint(n))==2
print('All flag, polynomial, and sign certificates verified exactly.')
print('D: degree',D.degree(),'; signs at 44,45:',sp.sign(D.eval(44)),sp.sign(D.eval(45)))
print('C2: degree',Cs[1].degree(),'; signs at 90,91:',sp.sign(Cs[1].eval(90)),sp.sign(Cs[1].eval(91)))
