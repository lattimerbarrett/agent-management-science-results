from fractions import Fraction
print('Two-increment scalar configurations a0=0, a1=eta*1, a2=2*eta*1:')
for k in [3,4,8,16,64,256]:
 eta=Fraction(1,2)-Fraction(1,k)
 if eta>0:
  margin=1-2*eta
  print(f'eta={eta}, margin={margin}, maximum tracial chain length={1//eta}')
print('\nAt eta=1/2: two increments are feasible, three are not.')
print('For any normalized trace and N increments, N*eta <= 1.')
print('Thus scalar or matrix configurations cannot be assembled into arbitrary-length witnesses while preserving their tracial increment values.')
