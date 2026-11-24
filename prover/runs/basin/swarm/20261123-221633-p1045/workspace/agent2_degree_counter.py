import sympy as S
s=S.Rational(1,1000);q=S.Rational(26,100);p=S.Rational(535274741,10**9);t=1-s
Rnorm=s+t*q*q
RBred=s*q+t*2*p*q/3
BBred=s*q*q+t*p*p/3
a=max(Rnorm,RBred,BBred)
Bnorm=s*(1-q)**2+t*(1+2*(1-p)**2)/3
RBblue=t*(1-q)*(1-2*p/3)
BBcrossblue=s*(1-q)**2+t*(2*(1-p)+(1-p)**2)/3
b=max(Bnorm,RBblue,BBcrossblue)
assert a==BBred and b==Bnorm
assert a<S.Rational(1,4) and b<S.Rational(1,2)
assert S.N(S.sqrt(a)+S.sqrt(b),30)<1
D=3*s*q+2*t*p
gap=S.factor(D-S.Rational(3,2)*(1+2*a-b))
assert gap<0
print('actual a,b:',S.N(a,15),S.N(b,15))
print('degree lemma gap:',S.N(gap,15))
print('random-curve condition:',S.N(S.sqrt(a)+S.sqrt(b),15))
