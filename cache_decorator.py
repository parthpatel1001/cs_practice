from __future__ import division
from functools import wraps

class Cache(dict):
	_cache = {}
	_metrics = {}
	def __init__(self, metrics=False):
		print 'called init'
		self.cache = Cache._cache
		self.metrics = Cache._metrics

	def __call__(self, fn):
		if fn not in self.cache:
			self.cache[fn] = {}
			self.metrics[fn] = {'hit':0,'miss':0}

		if self.metrics:
			@wraps(fn)
			def wrp(*args):
				try:
					res = self.cache[fn][args]
					self.metrics[fn]['hit']+=1
					return res
				except KeyError:
					res = self.cache[fn][args] = fn(*args)
					self.metrics[fn]['miss']+=1
					return res
			return wrp
		else:
			@wraps(fn)
			def wrp(*args):
				try:
					return self.cache[fn][args]
				except KeyError:
					res = self.cache[fn][args] = fn(*args)
					return res
			return wrp

	@staticmethod
	def debug_metrics():
		for fn, metric in Cache._metrics.iteritems():
			print fn.__name__, metric, '%d%%' % (100*metric['hit']/(metric['hit'] + metric['miss']))

def cache(metrics=False):
	'''helper to make it easier to wrap an imported function'''
	c = Cache(metrics)
	def w(fn):
		return c(fn)
	return w

@cache(metrics=True)
def test_me(a,b,c):
	return a + b + c

@cache(metrics=True)
def test_me_2(a,b,c):
	return 'wudup'

print test_me(1,2,3)
print test_me(1,2,3)
print test_me(1,2,3)
print test_me(1,2,3)
print test_me_2(1,2,3)
print test_me_2(1,2,3)
print test_me_2(1,2,3)
print test_me_2(1,2,3)
print test_me(1,2,3)


Cache.debug_metrics()