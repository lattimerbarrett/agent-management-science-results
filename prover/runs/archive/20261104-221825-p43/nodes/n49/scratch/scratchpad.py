import sympy as s
u,v,z,w,L=s.symbols('u v z w L',real=True)
for label,f in [('left endpoint',u*v+z*w),('right endpoint',(L-u)*v+z*w)]:
 H=s.hessian(f,(u,v,z,w))
 print(label,'Hessian eigenvalues:',H.eigenvals(),'det:',H.det())
print('Both proposed endpoint germs have Morse index 2. This is only a pointwise necessary condition, not proof that the prescribed arc germs extend to one coordinate chart.')
print('In the natural transverse frame of the actual arc, the transverse quadratic forms at its two ends are -b^2+d^2 and b^2-d^2. Thus endpoint chart identifications must be checked, not silently equated.')
