import sys,time
sys.path.insert(0,'workspace')
import complete_check
s=time.time();complete_check.main();print('rerun seconds',time.time()-s)
