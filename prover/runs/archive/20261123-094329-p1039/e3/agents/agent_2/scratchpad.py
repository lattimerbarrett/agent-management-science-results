from pathlib import Path
code='''import sympy as s
r=s.Rational(1,10)
delta=r**4
a2=3+delta
assert 2<a2<8 # c=sqrt(2/a2) satisfies 1/2<c<1
q=s.symbols('q',nonnegative=True)
rho_f=s.expand(a2+2*q+(q-1)**2-4)
assert rho_f==delta+q**2
assert s.simplify((r+r*r)/(1-r*r))==s.Rational(1,9)
assert s.simplify(r*r*(1+s.Rational(1,9)))==s.Rational(1,90)
assert s.Rational(1,90)<r/2
# The exact squared angular loss on the boundary is 2r^4.
assert delta+r**4==2*r**4
print('PASS: actual-candidate holomorphic safe-line obstruction constants.')
'''
Path('workspace/agent2_safe_line_obstruction_checks.py').write_text(code)
exec(compile(code,'workspace/agent2_safe_line_obstruction_checks.py','exec'))
text=r'''ACTUAL CANDIDATE: NO HOLOMORPHIC FAMILY OF SAFE HORIZONTAL LINES
This is an obstruction to one proof strategy, NOT an obstruction to Oka.
Work in n=3, z'=(z1,z2). Set r=1/10, δ=r^4, a=sqrt(3+δ), and
f(ζ)=((a,sqrt(2)ζ),ζ), |ζ|<=r. Then ρ(f(ζ))=δ+|ζ|^4>0.
Suppose b(ζ)=(b1,b2) is holomorphic and nonzero near this closed disk,
and for each ζ its affine horizontal line g(ζ)+C b(ζ) avoids the fiber
closed ball of squared radius R(ζ)^2=3+2|ζ|^2-|ζ|^4, where
g=(a,sqrt(2)ζ). Minimum squared norm on a complex affine line gives
|a b1+sqrt(2)conj(ζ)b2|^2 <= (δ+|ζ|^4)(|b1|^2+|b2|^2).
If b2=0 at any point, a^2<=δ+r^4, impossible. Thus h=b1/b2 is holomorphic.
Let c=sqrt(2)/a, so 1/2<c<1. On the boundary |ζ|=r, the inequality implies
|h+c conj(ζ)| <= c r^2 sqrt(|h|^2+1) <= c r^2(|h|+1).
Put k=c r^2<1/100. Triangle inequality gives
|h| <= (c r+k)/(1-k) < (r+r^2)/(1-r^2)=1/9.
Hence sup_boundary |h+c conj(ζ)|<1/90. On the other hand,
∮ (h+c conj(ζ))dζ =2πi c r^2,
so the integral inequality implies sup_boundary |h+c conj(ζ)|>=c r>1/20.
Contradiction. Thus such a holomorphic b does not exist, even though each
individual fiber point admits many safe lines.
'''
Path('workspace/agent2_safe_line_obstruction.txt').write_text(text)