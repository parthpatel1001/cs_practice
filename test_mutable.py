from functools import wraps
import time
def timeit(fn):
	@wraps(fn)
	def _timeit(*args, **kwargs):
		start = int(round(time.time() * 1000))
		res = fn(*args,**kwargs)
		end = int(round(time.time() * 1000))
		print kwargs.get('profile_name',fn.__name__),'took',end - start,'ms'
		return end-start
	return _timeit

@timeit
def test_sum_assign(items):
	total = 0
	for i in range(1,items):
		total += i
	return total

@timeit
def test_sum_compr(items):
	return sum([i for i in range(1,items)])

r = 1000000
for i in range(1,100):
	print test_sum_assign(r) - test_sum_compr(r)