import runpy
for filename in ["workspace/agent1_renderer.py", "workspace/agent2_phase_checks.py", "workspace/agent2_counter_cycles.py"]:
    print("RUNNING", filename, flush=True)
    runpy.run_path(filename, run_name="__main__")
