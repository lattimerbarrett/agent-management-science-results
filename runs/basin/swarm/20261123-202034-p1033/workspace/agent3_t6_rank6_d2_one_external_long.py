from pathlib import Path
s=Path('workspace/agent3_t6_rank6_d2_different_long.py').read_text()
s=s.replace('T=6;N=24;','T=6;N=25;')
s=s.replace("for orbit,petal in [('different',(4,8))]:","for orbit,petal in [('external',(4,24))]:")
s=s.replace('agent3_t6_rank6_d2_different','agent3_t6_rank6_d2_one_external')
s=s.replace('agent3_t6_rank6_d2_witness','agent3_t6_rank6_d2_one_external_witness')
exec(s)
