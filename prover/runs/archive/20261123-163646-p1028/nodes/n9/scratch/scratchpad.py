from sage.all import graphs, Graph
import inspect
print(type(graphs)); print(graphs.__doc__[:1200]); print(graphs(4)); print(type(graphs)); print(inspect.getsource(type(graphs).__call__))
