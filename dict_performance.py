from random import randint
import time
from functools import wraps

def timeit(fn):
	@wraps(fn)
	def _timeit(*args, **kwargs):
		start = int(round(time.time() * 1000))
		res = fn(*args,**kwargs)
		end = int(round(time.time() * 1000))
		print kwargs.get('profile_name',fn.__name__),'took',end - start,'ms'
		return res
	return _timeit

@timeit
def getDict(index_range, size):
	return {randint(0,index_range):0 for j in range(0,size)}




@timeit
def dict_access(d, look_for,**kwargs):
	for i in look_for:
		r = d[i] if i in d else None

index_range = 100000000
size = 1000000
d = getDict(index_range, size)

dict_access(d, range(0,size), profile_name='sequential_access')
dict_access(d, [randint(1,index_range) for i in range(1,size)], profile_name='random_access')


