import sympy as s
# Investigate the simplest time-dependent/symplectic two-fixed-point candidate.
# A swap followed by a half-turn has two fixed points, but is not Hamiltonian.
T=s.Matrix([[0,1],[1,0]])
print('factor-swap action on H^2 =', T)
print('Lefschetz number of swap composed with rotations =',1+s.trace(T)+1)
print('Hamiltonian maps must instead act identically on H^2, with Lefschetz number',1+2+1)
print('Thus the elementary swap construction does not give the stipulated Hamiltonian example.')
