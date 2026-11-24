import runpy, pathlib, sys, time
start=time.time()
runpy.run_path('workspace/compact_complete_agent1.py',run_name='__main__')
print('compact elapsed',time.time()-start)
# This second verifier constructs all intermediate face sets, and recursively
# recognizes all links. Suppress only its final write into the read-only team folder.
path='workspace/verify_lower_agent4.py'
src=pathlib.Path(path).read_text()
src=src[:src.index("if __name__=='__main__':")]
src='\n'.join(line for line in src.splitlines() if 'pickle.dump' not in line)
namespace={'__name__':'independent_rerun'}
exec(compile(src,path,'exec'),namespace)
namespace['main'](3)
namespace['main'](4)
print('all elapsed',time.time()-start)
