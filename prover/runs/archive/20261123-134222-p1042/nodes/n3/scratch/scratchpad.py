# Cohomology-operation degree check for the stipulated m=7 homology.
# Reduced integral homology: H_4=Z/2, H_5=Z^309.
H_free={4:0,5:309}
H_2tors={4:1,5:0}
mod2={d:H_free.get(d,0)+H_2tors.get(d,0)+H_2tors.get(d-1,0) for d in range(1,9)}
print('Reduced mod-2 Betti numbers:', {d:b for d,b in mod2.items() if b})
print('Positive Steenrod squares with possibly nonzero target:')
for d,b in mod2.items():
 if b:
  for i in range(1,d+1):
   if mod2.get(d+i,0):print(f'Sq^{i}: H^{d} -> H^{d+i}')
print('Sq^1 has rank 1: the integral torsion is Z/2, not Z/4.')
print('This is exactly the operation on M(Z/2,4) wedge 309 copies of S^5.')
