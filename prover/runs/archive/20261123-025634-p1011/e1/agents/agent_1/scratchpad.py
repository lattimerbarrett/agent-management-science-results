from pathlib import Path
files=['agent1_local_graph_lemma.md','agent3_formal_inverse_reduction.md','agent4_spectral_full_proof.md','agent2_robust_diagonal_complete.md']
Path('workspace/combined_n19_construction.md').write_text('\n\n---\n\n'.join(Path('workspace/'+f).read_text() for f in files))
print('Regenerated combined construction with latest direct parameter derivative and exact action-transfer sections.')
print('Total lines:',len(Path('workspace/combined_n19_construction.md').read_text().splitlines()))
