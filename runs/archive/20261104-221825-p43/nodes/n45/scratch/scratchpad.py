# Necessary rank/index conditions from local-to-global Floer homology.
# Use the mod-4 grading HF_k = H_{k+2}(S2 x S2).
global_ranks={0:2,1:0,2:2,3:0}
local_candidates=[{0:2},{2:2}]
summed={k:sum(d.get(k,0) for d in local_candidates) for k in range(4)}
print('Global Floer ranks modulo 4:',global_ranks)
print('Formal two-point local rank pattern:',local_candidates)
print('Sum:',summed)
print('Rank constraints satisfied:',summed==global_ranks)
print('Euler characteristics:',[sum((-1)**k*r for k,r in d.items()) for d in local_candidates])
print('This is formal compatibility, NOT a construction of a global Hamiltonian map.')