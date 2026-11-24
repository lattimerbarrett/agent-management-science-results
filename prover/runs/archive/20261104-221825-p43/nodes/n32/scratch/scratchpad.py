import sympy as s
h,F,dh,dF=s.symbols('h F dh dF',real=True)
t=s.symbols('t',real=True)
# One normal coordinate at a boundary critical point of g.
fs=(1-t)*h+t*F
normal=(1-t)*dh+t*dF
V=(h-F)/normal
print('Derivative of f_s along the proposed moving collar:',s.simplify(s.diff(fs,t)+normal*V))
print('Boundary value of V when h=F:',s.simplify(V.subs(F,h)))
a,b=s.symbols('a b',positive=True)
print('Normal derivative when the two derivatives have the same sign:',(1-t)*a+t*b)
print('For 0<=t<=1 this is positive. Compactness supplies a common submersion collar.')
print('V vanishes on the boundary and is O(distance). Gronwall keeps sufficiently close initial points in the collar for 0<=t<=1.')
print('A cutoff extends V smoothly into the ball, zero away from the collar. Its time-dependent flow exists on the compact ball, fixes the boundary, and gives f_s o Phi_s = h near the boundary.')
