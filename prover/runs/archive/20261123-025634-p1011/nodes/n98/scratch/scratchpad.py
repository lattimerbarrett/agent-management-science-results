from pathlib import Path
p=Path('experiments/e3/agent1_high_dim_analytic_bridge.md')
s=p.read_text()
for marker in ['The global linearized operators','The preceding expansion is thus','INDEPENDENT AUDIT']:
 i=s.find(marker)
 print('\n---',marker,'---\n',s[i:i+1700] if i>=0 else 'not present')
print('\nCertificate limitation:\n',Path('experiments/e3/agent4_certificate_notes.txt').read_text())
print('\nOther workspace availability:')
for n in ['e4','e5','e6','e7']:
 q=Path('experiments')/n
 print(n,q.exists())
