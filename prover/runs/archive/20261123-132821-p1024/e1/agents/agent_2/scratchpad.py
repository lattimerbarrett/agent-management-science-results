import sympy as s, json
k=4; N=10
# Hyperelliptic gaps in genus six, and standard bases of H0 O(dp), H1 O(dp).
gaps=list(range(1,12,2))
def h0_basis(d): return [n for n in range(d+1) if n%2==0 or n>=13]
def h1_basis(d): return [n for n in gaps if n>d]
def mult_phi(source_d,target_d,pole):
    src=h0_basis(source_d); tgt=h1_basis(target_d)
    return s.Matrix([[int(v==pole+u) for u in src] for v in tgt])
R=mult_phi(4,8,9)
Q=mult_phi(0,4,9)
assert R.rank()==2 and Q.rank()==1
# Check exact coefficient conjugacy for all relevant weights/transitions.
for n in range(21):
    for j in range(7):
        assert s.simplify((n+j*k-k)*s.binomial(1-s.Rational(n,k),j)-(n-k)*s.binomial(-s.Rational(n,k),j))==0
out={'gaps':gaps,'h1_zero_weight_graded':[len(h1_basis(n)) for n in (0,4,8)],'O_obstruction_matrix':str(R),'A_obstruction_matrix':str(Q),'O_zero_weight_h1':sum(len(h1_basis(n)) for n in (0,4,8))-R.rank(),'A_zero_weight_h1':sum(len(h1_basis(n)) for n in (0,4,8))-Q.rank()}
print(out)
print('graded O,A total',sum(len(h1_basis(n)) for n in range(11)))
open('workspace/agent2_g6_check.json','w').write(json.dumps(out,indent=2,default=int))
# General formula matrix checks including all edge cases 3k=2g-2.
for g in range(2,101):
    r=(g+2)//3; k=g-r; N=2*g-2
    assert 3*k>=N and k<N and k//2>=r-1
    for ell in range(r):
        b=[(j+1)*(-1)**j if j<=ell else 0 for j in range(r)]
        M=s.Matrix(r,k//2+1,lambda i,a:b[i+a] if i+a<r else 0)
        # Anti-triangular nonzero minor proves rank; later rows vanish.
        minor=M[:ell+1,:ell+1]
        assert minor.det(method='domain-ge') == (-1)**(ell*(ell+1)//2)*b[ell]**(ell+1)
        assert all(M[i,a]==0 for i in range(ell+1,r) for a in range(k//2+1))
        if 3*k==N:
            # Q: H0 O(2kp) -> H1 O(3kp), nonzero row of b coefficients.
            Q=s.Matrix([[b[j] if j<r else 0 for j in range(k+1)]])
            assert Q.rank()==1
print('General matrix/edge-case assertions passed for all 2<=g<=100 and every last-nonzero index.')
from pathlib import Path
Path('workspace/agent2_general_matrix_check.py').write_text(Path('scratchpad.py').read_text().split('from pathlib import Path')[0])

