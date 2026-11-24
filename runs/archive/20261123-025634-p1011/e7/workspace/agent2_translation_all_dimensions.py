import sympy as s
m,r,z=s.symbols('m r z',positive=True)
q3=(m*r-m-4)/2
qt=2*(1+r)/m
for a in [0,1]:
    H=4*(-1+z*r)*(2+4*a)/(m*(m+2))+z*(q3*(s.Rational(16,1)/(m*(m+2)*(m+4))+16*a/((m+2)**2*(m+4)))+qt*4*(m+4)**2*a/(m*(m+2)**2))
    print('a',a,s.factor(H))
    endpoint=s.factor(H.subs(z,1/(2*r)))
    print('upper at 1/2r:',endpoint)
    expected=-4*(m+4*r+4)/(m*r*(m+2)*(m+4)) if a==0 else -4*(m-8)*(m+4*r+4)/(m*m*r*(m+2)*(m+4))
    assert s.factor(endpoint-expected)==0
    assert s.diff(H,z,2)==0
from pathlib import Path
Path('workspace/agent2_translation_all_dimensions.py').write_text(Path(__file__).read_text())
Path('workspace/agent2_translation_all_dimensions.md').write_text(r'''# Translation Hessian at the small scale root

This supplements agent2_quartic_all_dimensions_proof.md and uses the translation decomposition established by agents 1 and 4. It proves a finite-dimensional local critical-point statement, not the PDE gluing theorem.

Let m=n-1, let the tracefree quadratic form have matrix diag(1,-1,0,...,0), and let A,B,C be its scalar spectral moments. Put r=B/A>0,s=C/A>0. The scale polynomial is -Az+2Bz^2-Cz^3. If r^2>3s/4, its smaller root is
z_minus=(2r-sqrt(4r^2-3s))/(3s)=1/(2r+sqrt(4r^2-3s)),
so 0<z_minus<1/(2r).

The coefficient of xi_i^2 in the positive shape norm Q, divided by Az, is affine in z. There are two cases, a_i^2=0 or1, since tr(A_mat^2)=2. The exact spectral constants q3/A=(mr-m-4)/2 and qtrace/A=2(1+r)/m give
h0(z)=8[2mrz-mz-m+4rz-4z-4]/[m(m+2)(m+4)],
h1(z)=8[6m^2rz-m^2z-3m^2+20mrz+4mz-12m+32rz+32z]/[m^2(m+2)(m+4)].
At z=0 both are negative. At the other endpoint,
h0(1/(2r))=-4(m+4r+4)/[mr(m+2)(m+4)]<0,
h1(1/(2r))=-4(m-8)(m+4r+4)/[m^2r(m+2)(m+4)]<0 for m>8.
Since both functions are affine, h0,h1 are strictly negative throughout [0,1/(2r)] when n>9. The matrix is diagonal by coordinate reflection symmetry. The mixed scale-translation derivatives vanish because the profile is even, hence first translation derivatives vanish identically in scale. Therefore the negative shape Hessian has a strict nondegenerate minimum at the smaller scale root whenever n>9 and the scale discriminant is positive.

The companion quartic scale certificate proves that discriminant positive for every n>=32. Combining the two gives a full nondegenerate local minimum of the projected second-order reduced functional for every n>=32. No nonlinear remainder estimates, fixed-metric infinite gluing, or conclusion for n=7,...,31 are claimed.
''')
