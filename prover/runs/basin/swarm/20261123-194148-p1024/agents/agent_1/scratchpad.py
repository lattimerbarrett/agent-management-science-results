from fractions import Fraction as Q

def choose(a,j):
    v=Q(1)
    for i in range(j): v *= (a-i)/(i+1)
    return v

def mul(a,b):
    c={}
    for i,x in a.items():
        for j,y in b.items(): c[i+j]=c.get(i+j,0)+x*y
    return {i:x for i,x in c.items() if x}

def cech_matrix(g,b,kind):
    r=(g+2)//3; k=g-r; N=4*g-3; M=4*g+2
    rows={}
    types=('h','v') if kind=='S' else ('f',)
    for n in range(N):
        for typ in types:
            for e in range(-3*n-4*g-(typ=='v'),0):
                rows[n,typ,e]=len(rows)
    psi={k-2*g+1+2*j:Q(x) for j,x in enumerate(b) if x}
    deriv={e-1:(e-k)*x for e,x in psi.items()}
    powers=[{0:Q(1)}]
    for j in range((N-1)//k): powers.append(mul(powers[-1],psi))
    columns=[]
    for n in range(N):
        for typ in types:
            horizontal=(kind=='L' or typ=='h')
            limit=4*n+(2*g+2 if horizontal else 4*g+(typ=='v'))
            alpha=(Q(1) if kind=='L' or typ=='v' else Q(0))-Q(n,k)
            for d in range(limit+1):
                if d%2 and d<2*g+1: continue
                col={}
                for j in range((N-1-n)//k+1):
                    factor=choose(alpha,j)*(-k)**j
                    if horizontal: factor *= -Q(1,2)
                    p={e:factor*x for e,x in powers[j].items()}
                    terms=[(n+j*k,typ,p,0)]
                    if typ=='h':
                        terms=[(n+j*k,'h',p,0),
                               (n+j*k,'v',{e:-x for e,x in p.items()},-1)]
                        if n+(j+1)*k<N:
                            terms.append((n+(j+1)*k,'v',
                                          {e:-x for e,x in mul(p,deriv).items()},0))
                    for m,tp,p,shift in terms:
                        for e,x in p.items():
                            base=n-d+(2-2*g if horizontal else 0)+e+shift
                            for a in range(max(0,(-1-base)//M+1)):
                                exponent=base+M*a
                                value=x*choose(Q(d%2+horizontal,2),a)*(-1)**a
                                if value:
                                    assert (m,tp,exponent) in rows
                                    i=rows[m,tp,exponent]
                                    col[i]=col.get(i,0)+value
                columns.append({i:x for i,x in col.items() if x})
    return len(rows),columns

def exact_rank(columns):
    pivots={}
    for col in columns:
        col=dict(col)
        while col:
            i=min(col); x=col[i]
            if i not in pivots:
                pivots[i]={j:y/x for j,y in col.items()}; break
            for j,y in pivots[i].items():
                col[j]=col.get(j,0)-x*y
                if not col[j]: del col[j]
    return len(pivots)

def cohomology(g,b):
    answer=[]
    for kind in ('O','S','L'):
        nr,columns=cech_matrix(g,b,kind)
        answer.append(nr-exact_rank(columns))
    return tuple(answer)

if __name__=='__main__':
    import random
    random.seed(2); checked=0
    for g in range(2,9):
        r=(g+2)//3
        cases=[[0]*r]+[[int(i==j) for i in range(r)] for j in range(r)]
        cases += [[random.randint(-2,2) for _ in range(r)] for _ in range(3)]
        for b in cases:
            hO,hS,hL=cohomology(g,b)
            s=max((j+1 for j,x in enumerate(b) if x),default=0)
            assert hO-hS+hL==1-s,(g,b,(hO,hS,hL))
            if s: assert hL-hO==4*g*g-7*g+2
            else: assert (hO,hS,hL)==(g*g,6*g*g-7*g+2,5*g*g-7*g+3)
            checked+=1
    print(checked,'exact Cech-matrix checks passed')
    from pathlib import Path
    Path('workspace/agent1_final_code.py').write_text(Path('scratchpad.py').read_text())
