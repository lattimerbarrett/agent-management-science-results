import sympy as s
from pathlib import Path
for N in range(4,11):
    b=[s.Integer(1),s.Integer(-1)]+[s.Integer(0)]*(N-3)
    def dd(i,j,k,l):
        return 2*b[i] if i==j and i<N-1 and k==l==N-1 else 0
    def R(i,j,k,l):
        return s.Rational(1,2)*(dd(i,l,j,k)+dd(j,k,i,l)-dd(i,k,j,l)-dd(j,l,i,k))
    Ric=s.Matrix(N,N,lambda j,l:sum(R(i,j,i,l) for i in range(N)))
    Sc=s.trace(Ric)
    assert Sc==0
    def W(i,j,k,l):
        delta=lambda a,b:int(a==b)
        return R(i,j,k,l)-s.Rational(1,N-2)*(delta(i,k)*Ric[j,l]-delta(i,l)*Ric[j,k]-delta(j,k)*Ric[i,l]+delta(j,l)*Ric[i,k])+Sc/s.Integer((N-1)*(N-2))*(delta(i,k)*delta(j,l)-delta(i,l)*delta(j,k))
    for a in range(N-1):
        for bb in range(N-1):
            assert W(a,N-1,bb,N-1)==-s.Rational(N-3,N-2)*b[a]*int(a==bb)
    assert W(0,N-1,0,N-1)!=0
    assert all(sum(W(i,j,i,l) for i in range(N))==0 for j in range(N) for l in range(N))
    print('n=',N,': generic independent tracefree normal quadratic jet has NONZERO Weyl.')
a0,a1,a2,a3,a4,a5,t=s.symbols('a0:6 t')
A=s.Matrix([[a0,a1,a2],[a1,a3,a4],[a2,a4,a5]])
I=s.eye(3)
assert s.simplify((I-t*A).T*(I-t*A)-(I-2*t*A+t*t*A*A))==s.zeros(3)
print('Exact flat Fermi metric identity g_t=(I-tA)^2 checked symbolically.')
Path('workspace/agent2_flat_normal_jet_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent2_flat_normal_jet_obstruction.md').write_text(r'''# Flat versus general normal metric jets

This is a geometric diagnostic, not a construction in the requested sharp range.

Let a smooth hypersurface lie in Euclidean space and use inward normal distance t. If its outward shape operator is S and induced metric is gamma, the normal flow is F(z,t)=F(z,0)-t nu(z). Its differential along the hypersurface is I-tS, and therefore exactly
 g_t(X,Y)=gamma((I-tS)X,(I-tS)Y)
 =gamma(X,Y)-2t II(X,Y)+t^2 gamma(SX,SY).
In boundary geodesic coordinates at p, gamma(p)=I,Dgamma(p)=0. The Gauss equation says R_gamma=II wedge II, so its quadratic tangential metric jet is O(II^2). Expanding II(z) yields second total-degree terms only of types z^2 II^2, t^2 II^2 and t z DII. There is NO independent tracefree normal-quadratic tensor in a flat ambient metric. The t z DII term is tangentially odd, so its bilinear interaction against the first jet tII vanishes by tangential parity for a radial boundary bubble. The remaining cubic-order interaction has coefficient O(II^3).

This follows in any locally conformally flat metric after passing to one local flat conformal representative, which is legitimate by the exact conformal covariance of the Yamabe/Robin problem. It does not depend on global conformal flattenability.

For contrast, take a generic metric in normal coordinates at a boundary point,
 g_nn=1,g_an=0,g_ab=delta_ab+t^2 B_ab,
where B is tangential symmetric tracefree and nonzero. At the point, first derivatives vanish and the second-derivative curvature formula gives
 R_anbn=-B_ab, Ric_ab=-B_ab, Ric_nn=0,R=0.
Consequently
 W_anbn=-(n-3)/(n-2) B_ab.
This is nonzero in every n>=4, so such an independent normal quadratic jet cannot occur in a locally conformally flat metric, even after multiplying by a positive conformal factor (Weyl vanishing is conformally invariant).

The checker constructs the complete second-jet curvature tensor for B=diag(1,-1,0,...), checks its Ricci/scalar traces, the exact Weyl formula and Weyl tracefreeness for n=4,...,10, and verifies the flat Fermi matrix identity symbolically.

Thus a general-boundary-metric gluing mechanism using independent metric degrees1(tA) and2(t^2B), whose scale cross term has degree3 without tangential parity cancellation, would not automatically give an LCF example. A reliable recent n>=7 reference must be checked against this exact distinction; the diagnostic alone does not identify its hypotheses or establish any alternate classification.
''')
