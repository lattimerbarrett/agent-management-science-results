from pathlib import Path
import runpy
src=Path('workspace/agent4_periodic_pointwise_certificate.py').read_text()
src=src.replace("OUT=Path('workspace/agent4_pointwise_certificate_chunks_v2')", "OUT=Path('recomputed_certificate')")
Path('audit_certificate_driver.py').write_text(src)
runpy.run_path('audit_certificate_driver.py',run_name='__main__')
