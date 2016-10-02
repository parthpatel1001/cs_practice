from functools import wraps
import time

def profile(fn):
	@wraps(fn)
	def _profile(*args, **kwargs):
		start = time.time()
		result = fn(*args, **kwargs)
		end = time.time()
		print '\t',fn.__name__,'took',(end-start)*1000,'ms'
		return result
	return _profile

