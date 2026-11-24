# Boundary-topology bookkeeping for two index-2 Morse blocks joined by a tube.
# Each zero-level link is a torus. Joining along disks produces a genus-2 surface.
chi_torus=0
chi_connected_sum=chi_torus+chi_torus-2
genus=(2-chi_connected_sum)//2
print('Candidate zero-level boundary surface Euler characteristic:',chi_connected_sum)
print('Candidate surface genus:',genus)
print('A genus-two separating surface in S^3 is not a certificate of a function-preserving collar.')
print('In particular, these Euler-characteristic data do not establish radial replaceability.')
# Global efficient trisection Euler formula: chi(M)=2+g-3k.
g,k=2,0
print('Euler characteristic for a (2,0) trisection:',2+g-3*k)
