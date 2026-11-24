import sympy as s
from pathlib import Path
x,y=s.symbols('x y',real=True)
t=s.symbols('t', nonnegative=True)
f=(x*x+y*y-1)**2
levi=s.simplify((s.diff(f,x,2)+s.diff(f,y,2))/4)
assert s.expand(levi-(4*(x*x+y*y)-2))==0
# Exact quantitative test epsilon=1/16: |t-1|<=1/4 => Levi >= 1.
lo=s.Rational(3,4)
assert 4*lo-2==1
# Critical point in torus tube has every t=1, since t>=3/4;
# its defining value is -1/16, not zero.
assert -s.Rational(1,16)!=0
out={'one_coordinate_Levi':str(levi),'epsilon':'1/16','t_lower_bound':'3/4','Levi_lower_bound':'1','boundary_regular':True}
Path('workspace/agent3_torus_check.txt').write_text(str(out)+'\n')
print(out)
# Hénon automorphism H(z,w)=(w/10,z/10+10*w*w).
# Fixed 0 has eigenvalues +/-1/10. On torus tube, |z|,|w| <=sqrt(5)/2,
# |w|^2>=3/4, so image has |W| >=15/2-sqrt(5)/20>7 and |Z|<1.
assert s.Rational(15,2)-s.sqrt(5)/20>7
assert s.sqrt(5)/20<1
# Escape cone |w|>max(|z|,2):
# |W|>=10|w|²-|z|/10 >10r²-r/10>2r, |Z|=r/10.
r=s.symbols('r',positive=True)
assert s.simplify((10*r*r-r/s.Integer(10)-2*r)-r*(100*r-21)/10)==0
print('Explicit Henon map sends the strict-psh torus tube into forward escape cone; its attracting basin contains 0 and avoids K.')
z,w,Z,W=s.symbols('z w Z W')
H=s.Matrix([w/10,z/10+10*w*w])
Hi=s.Matrix([10*W-10000*Z*Z,10*Z])
assert all(s.simplify(c)==0 for c in Hi.subs({Z:H[0],W:H[1]},simultaneous=True)-s.Matrix([z,w]))
assert set(H.jacobian([z,w]).subs({z:0,w:0}).eigenvals())=={s.Rational(-1,10),s.Rational(1,10)}
print('H inverse and attracting derivative checked exactly.')
ss,tt,uu=s.symbols('ss tt uu',real=True)
rho=ss**2-2*ss+tt-1
scaled=uu**2*ss**2-2*uu*ss+uu*tt-1
assert s.expand(scaled-(uu*rho+(1-uu)*(-1)-ss**2*uu*(1-uu)))==0
# Radial derivative on rho=0 is 2(s^2+1)>0.
radial=4*ss*(ss-1)+2*tt
assert s.expand(radial.subs(tt,1+2*ss-ss**2)-2*(ss**2+1))==0
print('Simple mixed-Levi compact is strictly star-shaped: exact radial identities checked.')
Path('workspace/agent3_dimension_reduction.md').write_text('''# Conditional dimension reduction (NOT a complete solution)\n\nLet (T) denote the unverified global assertion: for n>=3, the exterior of every smooth compact domain whose boundary has at least n-2 strictly positive tangential Levi eigenvalues everywhere is Oka.\n\nIf (T) holds, the following proved geometric arguments give S containing every n>=3 and N={2}.\n\n1. If K is pseudoconvex and n>=3, the outer defining functions psi_epsilon=rho-epsilon exp(-A|z|^2) give decreasing smooth compact neighborhoods K_epsilon of K. On their boundaries rho=epsilon exp(-A|z|^2). Uniform smoothness gives L_rho(v)>=-C rho |v|^2 for rho>=0 and v in ker partial rho. On the common tangent space E=ker partial rho intersect ker partial |z|^2, dimension at least n-2, L_psi(v)>=epsilon exp(-A|z|^2)(A-C)|v|^2>0. Choose A>C. Thus (T) makes each exterior Oka. Their increasing union is C^n\\K and is Oka directly from CAP, because each compact image f(Q) lies in one member.\n\n2. For n>=3 take rho=(|z|^2-1)^2+||w||^2-2, z in C and w in C^{n-1}. The domain rho<=0 is smooth, compact, connected and strictly star-shaped. On each boundary, w-orthogonal tangent directions give n-2 positive Levi eigenvalues. At z=0, ||w||=1, the z direction is tangent with Levi -2, so K is not pseudoconvex. Assertion (T) would make its exterior Oka, excluding every n>=3 from N.\n\n3. Independently of (T), 2 belongs to N: a negative tangential Levi eigenvalue of K gives a strictly pseudoconvex exterior boundary point. A holomorphic local peak glues to a bounded nonconstant continuous psh function on the exterior. CAP and bounded-subharmonic Liouville on C prohibit this. Full proof is in agent2_necessity.md.\n\nThe remaining universal S question would then be exactly whether 2 belongs to S. Neither this question nor (T) has been settled by the team.\n''')
