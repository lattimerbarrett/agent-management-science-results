# Floer grading for S^2 x S^2: n=2 and minimal Chern number N=2.
# In the homological convention HF_k corresponds to H_{k+n}, modulo 2N.
betti={0:1,2:2,4:1}
HF={k:sum(b for d,b in betti.items() if (d-2)%4==k) for k in range(4)}
print('Minimal Chern number N=2; absolute grading only modulo 4.')
print('Global Floer ranks over the Novikov field:',HF)
trial=[{0:2},{2:1},{2:1}]
print('Formal three-point rank distribution:',trial)
print('Its total:',{k:sum(t.get(k,0) for t in trial) for k in range(4)})
print('Conclusion: rank counting alone does not exclude three points; a stronger local-to-global restriction is necessary.')
