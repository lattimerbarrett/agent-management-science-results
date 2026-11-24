## Outer approximation lemma (proved)
Suppose n>=3 and K is the closure of a bounded domain with C-infinity pseudoconvex boundary. Then K has a decreasing neighborhood basis K_epsilon of compact domains with smooth boundary having a strictly positive tangential Levi direction at each point.

Choose a smooth signed-distance defining function rho in a fixed collar of boundary K, negative on K. Compactness, smoothness, and pseudoconvexity imply a constant C with
L_rho(z;v) >= -C rho(z)||v||²
for all z in the outer collar and v in ker(partial rho(z)). To see this, project z to its nearest boundary point q; rho(z) is the signed distance. The tangent hyperplanes and Levi matrices differ by O(rho(z)); projecting v to ker(partial rho(q)) changes it by O(rho(z))||v||. Apply nonnegativity at q and absorb the uniform errors.

Fix A>C and set psi_epsilon(z)=rho(z)-epsilon exp(-A||z||²) in the collar. For sufficiently small epsilon, its zero set is a unique small positive outward normal graph over boundary K, since its outward normal derivative is uniformly positive. Define K_epsilon to be K plus the part of the outer collar where psi_epsilon<=0. These are smooth compact connected domains, decrease to K as epsilon decreases to zero, and form a neighborhood basis.

At a boundary point z of K_epsilon, rho(z)=epsilon exp(-A||z||²). The complex subspace
E_z=ker(partial rho(z)) intersect ker(partial ||z||²)
has dimension at least n-2>=1. Every nonzero v in E_z is complex tangent to psi_epsilon=0. Direct differentiation gives
L_{-exp(-A||z||²)}(v)=exp(-A||z||²)[A||v||²-A²|sum bar(z_j)v_j|²].
The final term vanishes on E_z, so
L_{psi_epsilon}(v)>=epsilon exp(-A||z||²)(A-C)||v||²>0.

The exteriors C^n minus K_epsilon increase to C^n minus K. Hence any theorem asserting Oka for holes with one strictly positive tangential Levi direction would imply the desired universal sufficiency in every n>=3, since increasing unions of Oka domains are Oka directly by CAP compactness. No such global theorem is proved in this note.
