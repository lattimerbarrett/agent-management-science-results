from pathlib import Path
for name in ['agent2_s2_all_n_proof.md','agent3_s3_global_cases.md','agent2_conditional_edge_closure.md','agent2_vertex_pulse_lemma.md','agent4_reflection_edge_cycles.json']:
 p=Path('experiments/e4')/name
 print('\n===== '+name+' =====\n'+p.read_text()[:35000])
