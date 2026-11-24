from pathlib import Path
import types,sys
b=Path('experiments/e3')
m=types.ModuleType('agent3_general_blocks')
m.__dict__['__name__']='agent3_general_blocks'
exec((b/'agent3_general_blocks.py').read_text(),m.__dict__)
sys.modules['agent3_general_blocks']=m
ns={'__name__':'finite_certificate_import'}
exec((b/'agent2_finite_maxima_certificates.py').read_text(),ns)
ns['certificate'](19)
