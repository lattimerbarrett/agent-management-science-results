import z3
eta,t = z3.Reals('eta t')
s=z3.Solver()
s.add(eta>0, eta<=t, eta<=1-t, eta>z3.RealVal('1/2'))
print('Admissible eta > 1/2:',s.check())
s=z3.Solver();s.add(eta==z3.RealVal('1/2'),eta<=t,eta<=1-t)
print('Endpoint scalar constraints:',s.check())
if s.check()==z3.sat: print('Endpoint model:',s.model())
print('Scaling a_n by r in (0,1] changes eta to r*eta and preserves the absence of a supremum.')
