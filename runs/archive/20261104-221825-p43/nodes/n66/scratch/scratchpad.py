import sympy as s
Q=s.Matrix([[0,1],[1,0]])
print('Global middle intersection form:',Q)
print('Euler characteristic from prospective critical groups: 1+2+1 =',1+2+1)
print('For a cone critical point with negative region a genus-2 handlebody,')
print('local critical groups C_k = reduced H_{k-1}(handlebody): C_2 = Z^2, others zero.')
print('The local groups alone specify no symmetric intersection pairing on C_2.')
print('Thus rank and Euler-characteristic comparisons alone do not rule out three isolated critical points.')
print('Two invariant generators have square zero and mutual pairing one:', Q[0,0],Q[1,1],Q[0,1])
