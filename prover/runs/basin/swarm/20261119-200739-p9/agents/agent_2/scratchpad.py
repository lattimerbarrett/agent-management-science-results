from pathlib import Path
p=Path('workspace/agent2_upper.md');t=p.read_text();t=t.replace('These are standard real-variable lemmas, but S1 and S2 still require full proofs if a completely self-contained solution is demanded.','Complete proofs of S1, S2 and S3 are supplied below, including an elementary maximal-determinant substitute for the ellipsoid theorem.')
p.write_text(t)
print('Removed obsolete auxiliary-gap warning: all three lemmas are now proved below in the file.')