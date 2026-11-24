from pathlib import Path
for name in ['agent3_n3_compactness_assembled.md','agent2_n5_renormalized_SP.md','agent2_n6_renormalized_SP.md','agent4_n4_pohozaev_sign.md']:
 p=Path('experiments/e7')/name
 print('\nFILE',name,'\n',p.read_text()[:15500] if p.exists() else 'missing')
