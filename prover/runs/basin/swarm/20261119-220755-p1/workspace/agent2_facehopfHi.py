from pathlib import Path
p=Path('workspace/agent2_facehopf.py').read_text().replace('.5+2.319j','.5+3.198j').replace('a.imag-2.37','a.imag-3.24').replace('0+2.37j','0+3.24j').replace('agent2_facehopf_','agent2_facehopfHi_').replace("Path('workspace/agent2_facehopf.py')","Path('workspace/agent2_facehopfHi.py')")
exec(p)
