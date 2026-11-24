# A filtered abelian-group model separates a graded cokernel from the
# lower-central-series intersection kernel in the question.
# G=Z; C_1=Z, C_r=0 for r>=2.
# A_1=...=A_6=Z, A_7=3Z, A_8=9Z (and continue with powers of 3).
A7_generator, A8_generator = 3, 9
print('Order of A_7 / (C_7 + A_8):', A8_generator // A7_generator)
print('Order of (C_6 intersect A_7) / C_7:', 1)
print('Thus a degree-seven graded cokernel of order 3 alone does not establish a degree-six kernel.')