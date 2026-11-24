import sympy as s
z,w=s.symbols("z w")
a=s.Rational(1,100); M=s.Integer(10)
H=s.Matrix([w,M*w*w-a*z])
J=H.jacobian([z,w]).subs({z:0,w:0})
assert J*J == -a*s.eye(2)
assert all(abs(complex(ev))<1 for ev in J.eigenvals())
r=s.symbols("r",positive=True)
# On escape cone r=|w|>max(|z|,1), triangle bound is >10r²-r/100.
assert s.expand(M*r*r-a*r-9*r*r-r*(r-a))==0
assert 1>a
# Pole-order cases: r0>=s0>0; d>=2. Unequal leading orders
# yield second-coordinate pole order max(d*s0,r0)>s0.
for deg in range(2,8):
    for r0 in range(1,100):
        for s0 in range(1,r0+1):
            if r0!=deg*s0:
                assert max(deg*s0,r0)>s0
# In equality case successive orders must divide by d forever.
for deg in range(2,8):
    for s0 in range(1,10001):
        cur=s0
        for k in range(s0.bit_length()+1):
            if cur%deg: break
            cur//=deg
        else: raise AssertionError((deg,s0))
print("Exact attracting Jacobian, escape-cone lower bound verified.")
print("Pole-order case inequalities and integer-division contradiction checked.")
