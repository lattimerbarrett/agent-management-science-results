from pathlib import Path
p=Path('workspace/agent4_k1_random_fast.py').read_text()
p=p.replace('from agent4_fastdec import dec','from agent2_fast_edge_decomp import edge_decomp\ndef dec(fs,k): return edge_decomp(fs)\ndec.cache_clear=edge_decomp.cache_clear\ndec.cache_info=edge_decomp.cache_info').replace('[(8,100),(9,100),(10,50),(11,20)]','[(9,50),(10,20)]').replace("Path('workspace/agent4_k1_random_fast.py').write_text(Path(__file__).read_text())",'')
exec(compile(p,'agent4_search','exec'))
