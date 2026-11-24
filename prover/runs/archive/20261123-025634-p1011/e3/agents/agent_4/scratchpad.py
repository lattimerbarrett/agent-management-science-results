from pathlib import Path
import contextlib,io,time
files=['agent4_graph_checks.py','agent4_exact_sums.py','agent4_certificates.py','agent4_all_n_certificate.py','agent4_translation_ge40.py','agent4_mass_flux_checks.py']
for fn in files:
 p=Path('workspace')/fn
 out=io.StringIO();t=time.time()
 with contextlib.redirect_stdout(out):
  exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
 lines=out.getvalue().splitlines()
 print('PASS',fn,round(time.time()-t,3),'s;',len(lines),'result lines;',lines[-1] if lines else '')
print('All six agent4 check suites executed in fresh namespaces; all exact assertions passed.')