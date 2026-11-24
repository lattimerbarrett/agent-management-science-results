import runpy, os
code='''import runpy\nfor filename in ["workspace/agent1_renderer.py", "workspace/agent2_phase_checks.py", "workspace/agent2_counter_cycles.py"]:\n    print("RUNNING", filename, flush=True)\n    runpy.run_path(filename, run_name="__main__")\n'''
open('workspace/agent1_verify_counter.py','w').write(code)
exec(compile(code,'workspace/agent1_verify_counter.py','exec'))
