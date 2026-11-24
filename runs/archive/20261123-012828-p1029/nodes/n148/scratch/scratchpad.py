import sympy as s
eta,u,c=s.symbols('eta u c', real=True)
print('Two-increment upper-bound certificate:',s.expand((u-eta)+(1-u-eta)))
print('If both summands are nonnegative, eta <= 1/2.')
N=s.symbols('N',integer=True,positive=True)
print('For a linear quasitrace: N*eta = tau(a_N)-tau(a_0) <= 1.')
print('Scaling a_n by c in (0,1] changes eta to c*eta and preserves all least-upper-bound questions.')
print('None of these facts constructs a witness in a finite AW*-factor.')
