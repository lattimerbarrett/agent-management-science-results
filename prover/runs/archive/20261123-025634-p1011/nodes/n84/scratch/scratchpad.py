from pathlib import Path
for name in ['agent3_n3_local_lemmas.md','agent3_n3_pohozaev_proof.md','agent2_n5_n6_weighted_first_approximation.md']:
 print('\n===== '+name+' =====\n'+(Path('experiments/e7')/name).read_text())
