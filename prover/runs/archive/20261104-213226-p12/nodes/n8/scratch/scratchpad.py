# Dimension squeeze using the verified corrected pairing rank supplied in the task.
# Do not use the earlier descendant-matrix implementation.
from sympy import partition
number_of_monomials = int(partition(12))
faber_zagier_relation_rank = 33
verified_corrected_pairing_rank = 44
upper_bound = number_of_monomials - faber_zagier_relation_rank
lower_bound = verified_corrected_pairing_rank
print('Degree-12 monomials:', number_of_monomials)
print('Faber-Zagier upper bound:', upper_bound)
print('Verified corrected pairing lower bound:', lower_bound)
assert lower_bound == upper_bound
print('Dimension:', upper_bound)
