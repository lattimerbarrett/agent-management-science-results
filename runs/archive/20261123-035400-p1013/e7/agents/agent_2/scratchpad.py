from pathlib import Path
p=Path('workspace/agent2_counterexample_proof.md');s=p.read_text().replace('e(G[N(v)]))','e(G[N(v)])').replace('As long as the current order m>=10000,','As long as the current order m>10000,');p.write_text(s)
p=Path('workspace/agent2_counterexample_checks.py');s=p.read_text();s=s.replace('    assert nx.is_bipartite(H.subgraph(range(7)))','    assert nx.is_tree(H.subgraph(range(7)))\n    assert nx.is_bipartite(H.subgraph(range(7)))')
s=s.replace('    C=100;N=100**6;K=2*C+4\n    assert N//2-36*100**5-4*C>=4\n    assert N//6-1>4*K\n    assert N//2-C-2-2*K>=5','    C=10;N=10000;K=24\n    assert N//2-40*100-40==960\n    assert N//6-1>4*K\n    assert N//2-C-2-2*K>=5\n    assert 6*(10**8-N)>N*(N-1)//2')
p.write_text(s)
exec(compile(s,str(p),'exec'))
