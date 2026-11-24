from pathlib import Path
import runpy
for name in ('agent4_finite_checks','agent4_kpair_checks'):
    p=Path('workspace')/(name+'.py')
    before=p.read_bytes()
    assert b'# EXPORT' not in before
    assert b'__file__' not in before
    for _ in range(2):
        runpy.run_path(str(p),run_name='__main__')
        assert p.read_bytes()==before
print('Both shared programs passed twice through runpy and remained unchanged.')
