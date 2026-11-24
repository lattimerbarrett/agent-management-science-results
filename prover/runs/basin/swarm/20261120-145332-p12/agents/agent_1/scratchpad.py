import sympy as s
from functools import lru_cache
@lru_cache(None)
def parts(n,m=None):
    if m is None: return parts(n,n)
    if n==0: return ((),)
    return tuple((i,)+p for i in range(min(n,m),1-1,-1) for p in parts(n-i,i))
from collections import Counter
from itertools import product
from math import factorial, comb
P=1000000007
g=25
invdf={i:pow(__import__('math').prod(range(1,2*i+2,2)), -1,P) for i in range(24)}
@lru_cache(None)
def bell(p):
    if not p: return (1,)
    a,*rest=p
    counts=tuple(Counter(rest).items())
    ans=[0]*(len(p)+1)
    for choice in product(*(range(c+1) for v,c in counts)):
        ss=a+sum(v*k for (v,c),k in zip(counts,choice))
        mult=__import__('math').prod(comb(c,k) for (v,c),k in zip(counts,choice))
        rem=tuple(v for (v,c),k in zip(counts,choice) for _ in range(c-k))
        coeff=mult*invdf[ss]%P
        for k,b in enumerate(bell(rem)):
            ans[k+1]=(ans[k+1]+coeff*b)%P
    return tuple(ans)
@lru_cache(None)
def integral(p):
    return sum((-1)**(len(p)-k)*factorial(2*g-3+k)*b for k,b in enumerate(bell(p)))%P

def rank_mod(rows):
    piv={}
    for row in rows:
        row=[int(x)%P for x in row]
        for i in range(len(row)):
            if row[i]:
                if i in piv:
                    c=row[i]
                    row=[(x-c*y)%P for x,y in zip(row,piv[i])]
                else:
                    inv=pow(row[i],-1,P)
                    piv[i]=[x*inv%P for x in row]
                    break
    return len(piv)
N=12

def mul(a,b):
    c=[0]*(N+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b[:N+1-i]):
            c[i+j]=(c[i+j]+x*y)%P
    return c

def fz_rows():
    A=[factorial(6*n)//(factorial(3*n)*factorial(2*n))%P for n in range(N+1)]
    B=[A[n]*(6*n+1)*pow(6*n-1,-1,P)%P for n in range(N+1)]
    invA=[1]+[0]*N
    for n in range(1,N+1): invA[n]=-sum(A[k]*invA[n-k] for k in range(1,n+1))%P
    Q=mul(B,invA)
    logA=[0]+[sum(k*A[k]*invA[n-k] for k in range(1,n+1))*pow(n,-1,P)%P for n in range(1,N+1)]
    Qpow=[[1]+[0]*N]
    for i in range(N): Qpow.append(mul(Qpow[-1],Q))
    empty={p:__import__('math').prod(pow(-logA[i]%P,m,P)*pow(factorial(m),-1,P)%P for i,m in Counter(p).items())%P for d in range(N+1) for p in parts(d)}
    @lru_cache(None)
    def poly(sig):
        if not sig: return empty
        j=sig[0]; mj=sig.count(j); counts=tuple(Counter(sig).items())
        result={}
        for choose in product(*(range(m+1) for v,m in counts)):
            tau=tuple(v for (v,m),k in zip(counts,choose) for _ in range(k))
            if j not in tau: continue
            rem=tuple(v for (v,m),k in zip(counts,choose) for _ in range(m-k))
            l=len(tau); shift=sum(v//3 for v in tau); b=sum(v%3==1 for v in tau)
            scalar=(-1)**l*factorial(l-1)*pow(__import__('math').prod(factorial(k) for k in choose),-1,P)*tau.count(j)*pow(mj,-1,P)%P
            pp=poly(rem)
            for n in range(shift,N+1):
                c=scalar*Qpow[b][n-shift]%P
                if n==0: c=c*(2*g-2)%P
                if not c: continue
                for p,x in pp.items():
                    if sum(p)+n>N: continue
                    key=tuple(sorted(p+((n,) if n else ()),reverse=True))
                    result[key]=(result.get(key,0)+c*x)%P
        return result
    rows=[]
    for r in range(1,N+1):
        for w in range(max(0,3*r-g+1)):
            if (g-r-w-1)%2: continue
            for sig in parts(w):
                if any(v%3==2 for v in sig): continue
                pp=poly(sig)
                rel={p:x for p,x in pp.items() if sum(p)==r}
                for extra in parts(N-r):
                    rowdict={tuple(sorted(p+extra,reverse=True)):x for p,x in rel.items()}
                    rows.append([rowdict.get(p,0) for p in parts(N)])
    return rows

if __name__=='__main__':
    rows=[[integral(tuple(sorted(a+b,reverse=True))) for a in parts(12)] for b in parts(11)]
    print('pairing',len(rows),len(rows[0]),rank_mod(rows),bell.cache_info())
    rel=fz_rows()
    print('FZ',len(rel),rank_mod(rel),'quotient',77-rank_mod(rel))
    print('annihilates',all(sum(a*b for a,b in zip(x,y))%P==0 for x in rows for y in rel))
    for pp in [1009,1013]:
        P=pp
        invdf={i:pow(__import__('math').prod(range(1,2*i+2,2)), -1,P) for i in range(24)}
        bell.cache_clear(); integral.cache_clear()
        pairing=[[integral(tuple(sorted(a+b,reverse=True))) for a in parts(12)] for b in parts(11)]
        rel=fz_rows()
        print('prime',P,'pairing rank',rank_mod(pairing),'FZ rank',rank_mod(rel))
    import ast, inspect, time, pickle
    from fractions import Fraction
    class Rationalize(ast.NodeTransformer):
        def visit_BinOp(self,node):
            self.generic_visit(node)
            return node.left if isinstance(node.op,ast.Mod) and isinstance(node.right,ast.Name) and node.right.id=='P' else node
        def visit_Call(self,node):
            self.generic_visit(node)
            if isinstance(node.func,ast.Name) and node.func.id=='pow' and len(node.args)==3:
                return ast.BinOp(left=ast.Call(func=ast.Name(id='Fraction',ctx=ast.Load()),args=[node.args[0]],keywords=[]),op=ast.Pow(),right=node.args[1])
            return node
    for fun in [mul,fz_rows,bell,integral]:
        tree=Rationalize().visit(ast.parse(inspect.getsource(fun)))
        exec(compile(ast.fix_missing_locations(tree),'<rational>','exec'))
    invdf={i:Fraction(1,__import__('math').prod(range(1,2*i+2,2))) for i in range(24)}
    start=time.time()
    exactrel=s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix(fz_rows())).convert_to(s.QQ)
    print('Exact FZ rank',exactrel.rank(),time.time()-start,flush=True)
    exactpair=s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix([[integral(tuple(sorted(a+b,reverse=True))) for a in parts(12)] for b in parts(11)])).convert_to(s.QQ)
    print('Exact pairing rank',exactpair.rank(),time.time()-start,flush=True)
    with open('exact_matrices.pkl','wb') as f: pickle.dump((exactrel.to_Matrix(),exactpair.to_Matrix()),f)
    F=exactrel.to_Matrix(); A=exactpair.to_Matrix()
    def rr(M): return s.polys.matrices.DomainMatrix.from_Matrix(M).convert_to(s.QQ).rank()
    for bound in range(2,9):
        ids=[i for i,p in enumerate(parts(12)) if max(p)<=bound]
        S=s.eye(77)[ids,:]
        ar=rr(A[:,ids]); qr=rr(F.col_join(S))-33
        print('max kappa',bound,'monomials',len(ids),'pair rank',ar,'FZ image rank',qr,flush=True)
        if qr>ar:
            for v in A[:,ids].nullspace():
                full=s.zeros(1,77)
                for i,x in zip(ids,v): full[i]=x
                if rr(F.col_join(full))>33:
                    den=s.ilcm(*[x.q for x in v]); vv=[int(x*den) for x in v]; common=__import__('math').gcd(*vv); vv=[x//common for x in vv]
                    print('radical',[(parts(12)[i],x) for i,x in zip(ids,vv) if x],flush=True)
                    break
            break
