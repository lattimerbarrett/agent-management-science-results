import runpy,time
s=time.time()
runpy.run_path('agents/agent_1/scratchpad.py', run_name='__main__')
print('audit seconds',time.time()-s)
