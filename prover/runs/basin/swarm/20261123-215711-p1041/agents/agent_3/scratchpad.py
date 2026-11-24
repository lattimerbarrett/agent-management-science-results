from pathlib import Path
p=Path('workspace/agent3_universal_empty2_bootstrap.md')
s=p.read_text()
s=s.replace('If a48, then b/h have weights among48,56,60 (total<=156).\nThe tops alpha,beta of a/b are factored rank4 quadratics;', 'If a48, sorting gives b<=(156-48)/2=54, so b48 by KT; h has\nweight48,56 or60. The tops alpha,beta of a/b are factored rank4 quadratics;')
p.write_text(s)
print('Clarified b48 explicitly in empty2 lemma B')