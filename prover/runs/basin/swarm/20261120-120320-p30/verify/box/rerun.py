import runpy, time
start=time.time()
runpy.run_path('agents/agent_1/scratchpad.py', run_name='__main__')
print('Total seconds:',time.time()-start)
