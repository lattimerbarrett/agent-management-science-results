import math,itertools
import numpy as np
from scipy.special import gamma,gammaln

def permutations_even(n):
    out=[]
    for p in itertools.permutations(range(n)):
        seen=set();cycles=[]
        for i in range(n):
            if i in seen: continue
            cyc=[];j=i
            while j not in seen:
                seen.add(j);cyc.append(j);j=p[j]
            cycles.append(cyc)
        if all(len(c)%2==0 for c in cycles):
            inv=[0]*n
            for i,j in enumerate(p):inv[j]=i
            out.append((p,inv,(-1)**sum(len(c)>2 for c in cycles),all(len(c)==2 for c in cycles)))
    return out

def check_identity(n,exhaustive=False,trials=1000):
    ps=permutations_even(n)
    choices=[list(itertools.permutations([j for j in range(n) if j!=i])) for i in range(n)]
    rng=np.random.default_rng(293)
    profiles=itertools.product(*choices) if exhaustive else ([choices[i][rng.integers(len(choices[i]))] for i in range(n)] for _ in range(trials))
    count=0;solv=0
    for profile in profiles:
        rank=np.zeros((n,n),dtype=int)
        for i,row in enumerate(profile):
            for k,j in enumerate(row):rank[i,j]=k
        signed=0;match=False
        for p,inv,s,is_match in ps:
            if any(rank[i,p[i]]>rank[i,inv[i]] for i in range(n)):continue
            if any(rank[i,j]<rank[i,inv[i]] and rank[j,i]<rank[j,inv[j]] for i in range(n) for j in range(i+1,n) if j!=p[i] and j!=inv[i]):continue
            signed+=s
            if is_match:match=True
        assert signed==int(match),(n,profile,signed,match)
        solv+=match;count+=1
    print('identity',n,'profiles',count,'solvable',solv,'even permutations',len(ps))

check_identity(2,True)
check_identity(4,True)
check_identity(6,False,3000)
check_identity(8,False,200)
C=2**.25*math.e*gamma(.75)/math.sqrt(math.pi)
print('C=',C)

def asympt_sum(N):
    # b recurrence from (1-w)b'=-w b/2
    b0=1.;b1=0.;a=1.;ans=0.
    for k in range(2,N+1):
        b=((k-1)*b1-.5*b0)/k
        a_prev=a
        # compute product increment from k-1 to k (also missing k=1 first)
        if k==2:a=(N/(N+.5))*((N-1)/(N+1.5))
        else:a*= (N-k+1)/(N+k-.5)
        ans+=(-b)*(1-a)
        b0,b1=b1,b
    # tail sum of b: sum_{k>N}(-b_k)=sum_{k=0}^N b_k
    # partial sum can be obtained stable recurrence sum b_k = coefficient of e^(w/2)(1-w)^(-1/2)
    # recurrence for c: (1-w)c'=(1-w/2)c
    c0=1.;c1=1.
    for k in range(2,N+1):c0,c1=c1,(k*c1-.5*c0)/k
    ans+=c1
    return math.exp(.5)*ans
for N in (100,1000,10000,100000):
    v=asympt_sum(N)
    print('N',N,'model P',v,'scaled',v*(2*N)**.25)

from fractions import Fraction
from collections import defaultdict
import sympy as sp
from scipy.integrate import quad

def exact_integral(cycles):
    n=sum(map(len,cycles));adj=set();ex=[0]*n
    for c in cycles:
        for h,i in enumerate(c):
            adj.add(tuple(sorted((i,c[(h+1)%len(c)]))))
            if len(c)>2:ex[i]=1
    poly={tuple(ex):1}
    for i in range(n):
        for j in range(i+1,n):
            if (i,j) in adj:continue
            new=defaultdict(int,poly)
            for powers,v in poly.items():
                row=list(powers);row[i]+=1;row[j]+=1
                new[tuple(row)]-=v
            poly={a:v for a,v in new.items() if v}
    return sum((Fraction(v,math.prod(t+1 for t in powers)) for powers,v in poly.items()),Fraction(0))

p4=3*exact_integral([[0,1],[2,3]])-6*exact_integral([[0,1,2,3]])
assert p4==Fraction(26,27)
p6=15*exact_integral([[0,1],[2,3],[4,5]])-90*exact_integral([[0,1,2,3],[4,5]])-120*exact_integral([[0,1,2,3,4,5]])
print('exact P4',p4,'exact P6',p6,float(p6))

n,m,t=sp.symbols('n m t', positive=True)
a=(2*n+4*m)/(n+m+1);b=(n+7*m)/(2*(n+m+1))
mu=sp.factor(a/2+b-a*a/4)
print('mu:',mu)
print('mu with m=tn asymptotic:',sp.series(mu.subs(m,t*n).subs(n,1/sp.Symbol('h')),sp.Symbol('h'),0,2))
assert sp.simplify(mu.subs(m,0)-sp.Rational(1,2)-(n-1)/(2*(n+1)**2))==0
assert sp.limit(mu.subs(m,0),n,sp.oo)==sp.Rational(1,2)
limmu=sp.limit(mu.subs(m,t*n),n,sp.oo)
assert sp.diff(limmu,t).subs(t,0)==2
w=sp.symbols('w')
B=sp.exp(w/2)*sp.sqrt(1-w)
assert sp.simplify(sp.diff(B,w)+w*sp.exp(w/2)/(2*sp.sqrt(1-w)))==0
print('b coefficients:',sp.series(B,w,0,9))
integ=quad(lambda x:x**(-1.5)*(-math.expm1(-x*x)),0,1)[0]+quad(lambda x:x**(-1.5)*(-math.expm1(-x*x)),1,np.inf)[0]
assert abs(integ-2*gamma(.75))<1e-9
print('limit integral',integ,'2 Gamma(3/4)',2*gamma(.75))
# Check the exact product form and Gaussian envelope.
for N in range(1,70):
    A=Fraction(1)
    for k in range(N+1):
        if k:A*=Fraction(2*(N-k+1),2*(N+k)-1)
        direct=Fraction(math.factorial(2*N)*2**(2*k),2)*Fraction(math.factorial(N+k-1),math.factorial(N-k)*math.factorial(2*N+2*k-1))
        assert A==direct
        assert float(A)<=math.exp(-k*k/(4*N))+1e-14
print('all algebraic, exact-integral, and finite checks passed')
