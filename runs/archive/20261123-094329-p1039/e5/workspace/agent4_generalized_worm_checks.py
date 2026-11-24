import sympy as S
x,y,e,ep,epp,s=S.symbols('x y eta eta_prime eta_second transverse_normsq', real=True)
R=1-e
b=ep-2*y
c=2*x+epp
N=(b+y)**2+(x-1)**2+(c-1)*R
SOS=(ep-y)**2+(x-e)**2+e*(1-e)+epp*(1-e)
boundary=(x-1)**2+y*y+s-R
assert S.expand(N-SOS)==0
# Boundary enters through the tangent projection norm, not this identity.
print('N minus SOS is identically:', S.factor(N-SOS))
# Complete-square identity in the (z,w) block of the Levi form.
p,q,r,t=S.symbols('p q r t',real=True)
vz=p+S.I*q; vw=r+S.I*t
levi=S.expand_complex(vz*S.conjugate(vz)+2*S.re(S.I*vz*S.conjugate(vw))+c*vw*S.conjugate(vw))
completed=S.expand_complex((vz-S.I*vw)*S.conjugate(vz-S.I*vw)+(c-1)*vw*S.conjugate(vw))
assert S.simplify(levi-completed)==0
# Tangent constraint after the square completion.
a=x-1+S.I*y
assert S.expand((b+S.I*S.conjugate(a))*S.conjugate(b+S.I*S.conjugate(a))-((ep-y)**2+(x-1)**2))==0
print('Exact complex Levi square-completion and tangent minimum numerator verified.')
open('workspace/agent4_generalized_worm_checks.py','w').write(open('scratchpad.py').read())
open('workspace/agent4_generalized_worm_checks.txt','w').write('Verified: N-SOS=0 identically.\nN=(eta_prime-y)^2+(x-1)^2+(2*x+eta_second-1)*(1-eta).\nSOS nonnegative for 0<=eta<=1, eta_second>=0.\nBoundary equation gives tangent projection norm R=1-eta.\n')