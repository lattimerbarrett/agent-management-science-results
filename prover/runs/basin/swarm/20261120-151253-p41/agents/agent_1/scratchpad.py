from sage.all import *
import sage.topology.simplicial_complex as sc
print(sc.__loader__)
print(sc.__spec__)
import inspect
try:
 print(inspect.getsource(sc.SimplicialComplex.is_shellable.f)[:1000])
except Exception as e: print(type(e),e)
try:
 src=sc.__loader__.get_source(sc.__name__)
 print('source available',len(src))
except Exception as e: print(type(e),e)
