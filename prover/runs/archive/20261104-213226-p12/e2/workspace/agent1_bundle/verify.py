"""Exact arithmetic certificate for dim R^12(M_25)=44.
Run: python verify.py .  Requires only the Python standard library.
The geometric meaning of the checked identities is in proof.md.
"""
import sys,json,math,time
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(100000)
from certificate_rows import row_exact,total
from dual import dual_values,bell
P=1000003
def isprime(n):
    return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
assert isprime(P) and isprime(1000000007)

def tup(x):
    return tuple(tup(v) for v in x) if isinstance(x,list) else x

def eligible(r,sig,aa):
    assert all(i>0 and i%3!=2 for i in sig)
    assert tuple(sorted(sig))==sig and all(a in (0,1) for a in aa)
    assert 3*r>=25+sum(sig)+sum(aa)
    assert (r-23-sum(sig)-sum(aa))%2==0

def check_label(lab):
    if lab[0] in ('rel','single'):
        if lab[0]=='rel':d,n,x=13,2,lab[1]
        else:d,n,x=lab[1],1,lab[2];assert d in (12,13)
        r,aa,sig,mul=x
        assert len(aa)==n and len(mul)==n+1
        eligible(r,sig,aa)
        assert all(i>0 for i in mul[0]) and tuple(sorted(mul[0]))==mul[0] and min(mul[1:])>=0
        assert sum(mul[0])+sum(mul[1:])==d-r
    elif lab[0]=='beta':
        mu,a,b=lab[1];assert all(i>0 for i in mu) and tuple(sorted(mu))==mu;assert b>=a>=0 and a+b>0 and sum(mu)+a+b==12
    elif lab[0]=='gamma':
        mu,a=lab[1];assert all(i>0 for i in mu) and tuple(sorted(mu))==mu;assert a>=0 and sum(mu)+a==11
    else:raise AssertionError(lab)

start=time.time()
cert=json.loads((BASE/'certificate.json').read_text())
assert cert['prime']==P
residual=defaultdict(Fraction);beta=[];rho=[]
for entry in cert['entries']:
    lab=tup(entry['label']);check_label(lab)
    c=Fraction(entry['coefficient']);assert c.denominator%P
    for j,a in row_exact(lab).items():residual[j]+=c*a
    cm=c.numerator*pow(c.denominator,P-2,P)%P
    if lab[0]=='beta':mu,a,b=lab[1];beta.append((mu,a,b,cm))
    if lab[0]=='gamma':mu,a=lab[1];rho.append((mu,a,cm))
assert total==1908 and all(v==0 for v in residual.values())
print('Exact rational Pixton certificate: all 1908 identities verified.')
print('Witness rows:',len(cert['entries']),' beta terms:',len(beta),' rho terms:',len(rho))

def detmod(A,p):
    A=[r[:] for r in A];out=1
    for k in range(len(A)):
        q=next((i for i in range(k,len(A)) if A[i][k]%p),None)
        if q is None:return 0
        if q!=k:A[q],A[k]=A[k],A[q];out=-out
        v=A[k][k]%p;out=out*v%p;iv=pow(v,p-2,p)
        for i in range(k+1,len(A)):
            c=A[i][k]*iv%p
            if c:
                for j in range(k+1,len(A)):A[i][j]=(A[i][j]-c*A[k][j])%p
            A[i][k]=0
    return out%p

def upper(p):
    ns={};exec((BASE/'fz_engine.py').read_text().replace('P=1000000007',f'P={p}'),ns)
    parts=ns['parts'];pmul=ns['pmul'];mm=ns['mulmono'];cols=parts(12);idx={q:i for i,q in enumerate(cols)}
    rows=[]
    for r in range(9,13):
        for size in range(3*r-26+1):
            if (size-r)%2:continue
            for sig in parts(size):
                if any(x%3==2 for x in sig):continue
                rel={m:c for m,c in pmul(ns['E'],ns['f'](sig)).items() if sum(m)==r}
                for q in parts(12-r):
                    row=[0]*len(cols)
                    for m,c in rel.items():row[idx[mm(m,q)]]=c
                    rows.append(row)
    base={};ri=[]
    for i,row in enumerate(rows):
        row=row[:]
        for j in range(len(cols)):
            if not row[j]:continue
            if j in base:
                c=row[j];row=[(a-c*b)%p for a,b in zip(row,base[j])]
            else:
                c=pow(row[j],p-2,p);base[j]=[a*c%p for a in row];ri.append(i);break
    ci=sorted(base)
    minor=[[rows[i][j] for j in ci] for i in ri]
    return cols,rows,ci,detmod(minor,p)

Q=1000000007
cols,rels,piv,upperdet=upper(Q)
assert len(cols)==77 and len(rels)==59 and len(piv)==33
assert upperdet==368438425
print('Upper 33 by 33 minor mod',Q,':',upperdet)
survivors=[m for i,m in enumerate(cols) if i not in piv];assert len(survivors)==44
qs=[tuple(q) for q in json.loads((BASE/'lower_columns.json').read_text())]
assert len(qs)==43 and all(sum(q)==11 for q in qs)
A,B=dual_values(beta,rho,survivors)
F=[(12*a+b)%P for a,b in zip(A,B)]
def hodge25(mu):
    mu=tuple(sorted(mu))
    return sum((-1)**(len(mu)-k)*math.factorial(47+k)*v for k,v in enumerate(bell(mu)))%P
lower=[[hodge25(m+q) for q in qs]+[f] for m,f in zip(survivors,F)]
lowerdet=detmod(lower,P)
assert lowerdet==540716
print('Lower 44 by 44 minor mod',P,':',lowerdet)
# Independent consistency check: the new functional annihilates all known relations.
c2,r2,_,_=upper(P);aa,bb=dual_values(beta,rho,c2);ff=[(12*a+b)%P for a,b in zip(aa,bb)]
assert all(sum(x*y for x,y in zip(row,ff))%P==0 for row in r2)
print('All 59 known target FZ relations annihilated by the new functional.')
print('VERIFIED: dimension <= 44 and dimension >= 44; hence dimension = 44.')
print('Elapsed seconds:',round(time.time()-start,2))
