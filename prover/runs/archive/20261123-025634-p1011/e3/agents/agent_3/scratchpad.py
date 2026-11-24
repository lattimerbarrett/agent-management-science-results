from pathlib import Path
p=Path('workspace/agent3_local_pohozaev_bridge_proposed.md');t=p.read_text()
t=t.replace('# Proposed local compensated-Pohozaev lemma: detailed analytic assembly','# Local compensated-Pohozaev lemma: detailed analytic assembly')
start=t.index('STATUS:');end=t.index('\n\n## Statement',start)
t=t[:start]+'''STATUS: independently audited end-to-end by agents 2 and 4 after the
corrections recorded below. The conditional local lemma is established using
standard Sobolev/trace, elliptic, spectral Green-kernel and implicit-function
theorems together with the explicitly proved identities and estimates.
This file is the analytic bridge, not merely a finite-matrix calculation.'''+t[end:]
t=t.replace('''Independent re-audit of this assembled
argument is still requested before treating the lemma as established.''','''Independent end-to-end re-audits by agents 2 and 4 found no remaining
unproved dimension-specific analytic step. The unified theorem still needs
to present the connected selection/cluster and global mass/rigidity modules,
not merely cite this local lemma without its stated proof.''')
p.write_text(t);Path('workspace/agent3_local_pohozaev_bridge.md').write_text(t)
print('Saved audited local lemma to workspace/agent3_local_pohozaev_bridge.md and updated original; lines',len(t.splitlines()))
