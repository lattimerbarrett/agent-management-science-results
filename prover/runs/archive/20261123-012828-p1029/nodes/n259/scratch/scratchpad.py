import sympy as s
A,B,C,R,L=s.symbols('A B C R L',real=True)
defect=C-A-B
complement_defect=s.expand((2*R-C)-((R-A)+(R-B)))
assert s.simplify(complement_defect+defect)==0
print('Original additivity defect:',defect)
print('Defect after replacing a,b by R1-a,R1-b:',complement_defect)
# If C < A+B, normalize a+b <= L1 and add its positive complement.
partition_sum=A/L+B/L+(1-C/L)
print('Sum of quasitrace values of normalized positive partition:',s.simplify(partition_sum))
print('Excess over 1:',s.simplify(partition_sum-1))
print('This certifies a finite defect only; the infinite construction is a separate supplied input.')
