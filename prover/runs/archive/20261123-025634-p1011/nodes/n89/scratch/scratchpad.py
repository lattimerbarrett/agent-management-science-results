# Check the algebraic reduction of the forced Robin boundary flux.
import sympy as s
z,b,H,u,g,W,T,a,m=s.symbols('z b H u g W T a m')
# T=x^T.grad_T u, Jgrad=|grad_T u|^2, pot=(K/q)u^q.
Jgrad,pot,TH=s.symbols('Jgrad pot TH')
v=g-b*H*u
raw=(T+z*v)*v-z*(Jgrad+v*v)/2+a*u*v+z*pot
# Before tangential integration: -b H u T is kept explicit.
pre=-b*H*u*T+g*(T+a*u-b*H*z*u)+z*g*g/2+b*b*H*H*z*u*u/2-a*b*H*u*u-z*Jgrad/2+z*pot
assert s.expand(raw-pre)==0
# Integrating -b H u T by parts contributes
# b/2*(TH+H*(m-H*z))*u^2 and the edge -b/2 H u^2 x^T.eta.
post=s.expand(pre+b*H*u*T+b*s.Rational(1,2)*(TH+H*(m-H*z))*u*u)
post_expected=g*(T+a*u+z*v)-z*g*g/2 + b*s.Rational(1,2)*((m-2*a)*H+TH+(b-1)*H*H*z)*u*u-z*Jgrad/2+z*pot
assert s.expand(post-post_expected)==0
assert s.simplify((m-2*a).subs({m:s.Symbol('n')-1,a:(s.Symbol('n')-2)/2}))==1
print('Verified forced boundary flux, tangential integration, edge sign, and coefficient m-2a=1.')
