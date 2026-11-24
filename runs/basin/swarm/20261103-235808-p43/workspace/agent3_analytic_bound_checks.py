from fractions import Fraction as F
from math import factorial
from pathlib import Path
# Triangle-inequality bounds for cancelled formulas in agent3_chart_formulas.py.
h=F(1,10**20);delta=F(1,10**12);A=F(10**7);qmax=F(200);qmin=F(1,200)
# X,Y norms<A; disk factor discrepancy < h² A²;
# transverse v-X,w-Y norms < h² A³.
disk_error=h*h*A*A
S_error=2*h*h*A**3
complex_q_error=4*qmax*delta+4*delta**2
R_error=complex_q_error+2*(qmax+1)*S_error+S_error**2+h*h*A**4
D_error=R_error+h*h*(1+10**5)
assert disk_error<F(1,10**25)
assert D_error<F(1,10**8)
assert qmin*qmin-D_error>F(1,10**5)
Rmax=F(10**5);Dmin=F(1,10**5)
# Complex norms |c|<=2, |c²|<=2, |v|,|w|<=2A, |S|<=201, |Z|<=A².
Ubound=(h*h*2*A+2*Rmax*2*A+4*(201*2+h*h*A*A*2*A))/Dmin
assert Ubound<10**20
# z_bend+1 =h²/D *[xz+1+c² R² X²/2+2c cross(S,v)+c²R² Z].
zcoeff=(3+2*Rmax*A*A/2+4*201*2*A+2*Rmax*A*A)/Dmin
assert zcoeff<10**25
out_z_coeff=2*zcoeff+4*Ubound+4
assert out_z_coeff<10**26
assert h*h*out_z_coeff<F(1,10**13)
# inverse equalarea sqrt factor then bounded by2.
M=F(10**30);assert 8*Ubound<M
# Cauchy on half-radii: coordinate derivatives through total order3.
cauchy=2*M/h*factorial(3)*(2/delta)**3
assert cauchy<10**100
print('PASS rational analytic bounds: Dmin>1e-5, scaled outputs<1e30, C3 chart error<1e100/k.')
print('D error bound:',float(D_error),'output z coefficient bound:',float(out_z_coeff))
