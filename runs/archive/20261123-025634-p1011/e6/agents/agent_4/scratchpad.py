from pathlib import Path
for name in ['agent4_projected_inverse_lemma.md','agent4_C1_graph_upgrade.md','agent4_flat_graph_estimates.md']:
 p=Path('workspace')/name
 p.write_text(p.read_text()+'\nDensity convention: smooth compactly supported halfspace approximants mean\n`C_c^infinity(overline{R_+^n})`, smooth up to the boundary with unrestricted\ntrace; no Dirichlet-zero boundary condition is imposed.\n')
print('Made Neumann density convention explicit in all agent4 analytic notes')
