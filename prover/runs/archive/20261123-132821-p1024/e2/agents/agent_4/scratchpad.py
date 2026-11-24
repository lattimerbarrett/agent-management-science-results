from pathlib import Path
s=Path('workspace/agent4_cech.py').read_text()
s=s[:s.index("if __name__=='__main__':")]
s=s.replace('from collections import defaultdict','from collections import defaultdict\nfrom fractions import Fraction')
s=s.replace('P=1000003','''class RationalField:
    def __rmod__(self,x): return x
P=RationalField()''')
s=s.replace('def inv(x): return pow(x%P,P-2,P)','def inv(x): return Fraction(1,x)')
s=s.replace('pow(-k,q,P)','((-k)**q)')
s=s.replace('"""Exact finite-Cech rank checks over a finite prime field.','"""Exact finite-Cech rank checks over the rational field.')
# copy same algorithm but all arithmetic rational
s+='''
if __name__=='__main__':
    from sympy import Matrix, symbols, prod
    checked=0
    # Universal symbolic Hankel pivot, including all lower coefficients.
    for m in range(16):
        b=symbols('b:'+str(m+1))
        H=Matrix(m+1,m+1,lambda i,j:b[i+j] if i+j<=m else 0)
        # Reversing columns gives triangular matrix with diagonal b_m.
        J=H[:,::-1]
        assert all(J[i,j]==0 for i in range(m+1) for j in range(i))
        assert prod(J[i,i] for i in range(m+1))==b[m]**(m+1)
    for g in range(2,10):
        r=(g+2)//3;k=g-r
        for m in range(r):
            for b in ([int(j==m) for j in range(r)],
                      [j+2 if j<=m else 0 for j in range(r)]):
                H=Matrix(r,k//2+1,lambda i,j:b[i+j] if i+j<r else 0)
                assert H.rank()==m+1
                hs=[h1(g,b,a,h) for a,h in [(0,0),(1,0),(0,1),(1,1)]]
                assert hs[1]-hs[0]==m and hs[2]==hs[3],(g,b,hs)
                # Stability: enlarge both Laurent and fiber cutoffs.
                hs2=[h1(g,b,a,h,M=4*g+4,N=4*g-2) for a,h in [(0,0),(1,0),(0,1),(1,1)]]
                assert hs2==hs,(g,b,hs,hs2)
                checked+=1
        print('Rational full-Cech verified through genus',g,flush=True)
    print('Passed',checked,'rational Cech/stability cases and 16 universal symbolic Hankel identities')
'''
Path('workspace/agent4_exact_cech.py').write_text(s)
exec(compile(s,'workspace/agent4_exact_cech.py','exec'))