from pathlib import Path
import time
p=Path('workspace/agent1_final_certificate.py')
start=time.time()
exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
print('agent3 independent consolidated verifier rerun seconds',time.time()-start,flush=True)
