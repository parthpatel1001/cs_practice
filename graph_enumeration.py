from math import factorial
import time
from functools import wraps
import sys

class Cache(dict):
	_cache = {}
	_metrics = {}
	def __init__(self, metrics=False):
		self.cache = Cache._cache
		self.metrics = Cache._metrics

	def __call__(self, fn):
		if fn not in self.cache:
			self.cache[fn] = {}
			self.metrics[fn] = {'hit':0,'miss':0,'size':0,'max_size':0}

		if self.metrics:
			@wraps(fn)
			def wrp(*args):
				self.metrics[fn]['size'] = int(sys.getsizeof(Cache._cache[fn])) / 1000.0
				if self.metrics[fn]['size'] > self.metrics[fn]['max_size']:
					self.metrics[fn]['max_size'] = self.metrics[fn]['size']
				try:
					res = self.cache[fn][args]
					self.metrics[fn]['hit']+=1
					return res
				except KeyError:
					res = self.cache[fn][args] = fn(*args)
					self.metrics[fn]['miss']+=1
					return res
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
		print 'Function','hit_rate','calls','hits', 'miss','cache_size', 'max_size','debug'
		for fn, metric in Cache._metrics.iteritems():
			d = metric['hit'] + metric['miss']
			p = 0
			if d:
				p = round(100 * float(metric['hit']) / float(d),2)
			
			print fn.__name__, '%s%%' % (p),d, metric['hit'],metric['miss'],'%skb' % metric['size'], '%skb' % metric['max_size'],'-' 

	@staticmethod
	def clear_cache():
		for fn in Cache._metrics:
			Cache._metrics[fn] = {'hit':0,'miss':0,'size':0,'max_size':0}
			Cache._cache[fn] = {}

class Profile(dict):
	perf = {}
	def __init__(self, *theories, **kwargs):
		self.theories = theories
		self.times = kwargs.get('times',1)
		self._perf = Profile.perf
		self.bw = kwargs.get('between',None)
	
	def _time(self, fn, *args, **kwargs):
		start = int(round(time.time() * 1000))
		res = fn(*args,**kwargs)
		end = int(round(time.time() * 1000))
		self._perf.setdefault(fn,[]).append(end - start)
		return res

	def __call__(self, fn):
		@wraps(fn)
		def wraps_theory(*args, **kwargs):
			for i in range(0,self.times):
				res = self._time(fn, *args, **kwargs)
				if self.bw is not None:
					self.bw()

			for theory in self.theories:
				for i in range(0,self.times):
					self._time(theory, *args, **kwargs)
					if self.bw is not None:
						self.bw()
			return res
		return wraps_theory

	@staticmethod
	def debug_perf():
		print 'Function','avg_time'
		for fn, perf in Profile.perf.iteritems():
			a = 0 if not len(perf) else float(sum(perf)) / len(perf)
			print fn.__name__,'%dms' % a

class Test(dict):
	def __init__(self,check,between=None):
		self.check = check
		self.bw = None

	def __call__(self, fn):
		@wraps(fn)
		def wrap_test(*args,**kwargs):
			expected = self.check(*args,**kwargs)
			if self.bw:
				self.bw()
			res = fn(*args,**kwargs)
			if expected != res:
				msg = 'Test failed %s' % (str(('args:',args,'result',res,'expected',expected,'kwargs:',kwargs)))
				raise Exception(msg)
			return res
		return wrap_test

def cache(fn):
	'''helper to make it easier to wrap an imported function'''
	return Cache(metrics=True)(fn)

def profile(*theories, **kwargs):
	_p = Profile(*theories, **kwargs)
	def wraps_profile(fn):
		return _p(fn)
	return wraps_profile

def test(check,between=None):
	_t = Test(check,between)
	def wraps_test(fn):
		return _t(fn)
	return wraps_test

factorial = cache(factorial)

@cache
def choose(n,r):
	d = n - r
	if d < 0:
		return 0
	return factorial(n)/factorial(r)/factorial(d)

@cache
def qq(n, k):
    '''Number of labeled, simply connected Graphs of order n, size k '''
    s = n * (n - 1) / 2
    if k < n - 1 or k > s:
        res = 0
    elif k == n - 1:
        res = int(pow(n, (n - 2)))
    else:
        res = choose(s, k)
        for m in range(0, n - 1):
            res1 = 0
            lb = max(0, k - (((m + 1) * m) / 2))
            for p in range(lb, k - m + 1):
                np = ((n - 1 - m) * (n - 2 - m)) / 2
                res1 += choose(np, p) * qq(m + 1, k - p)

            res -= choose(n - 1, m) * res1
    return res

# @cache
def choices(i,n,k):
	t = 0
	# check_until = range(min(choose(i, 2), k), i - 2, -1)
	check_until = range(i - 1, min(choose(i, 2), k) + 1)

	edge_pairs = choose(n - i, 2)
	for j in check_until:
		c = choose(edge_pairs, k - j)
		if not c:
			continue
		t += c * answer(i,j)
	return t

# @cache
def invalid(n, k):
	t = 0
	p = n - 1
	
	for i in range(1, n):
		sub_graph = choose(p, i-1)
		if not sub_graph:
			continue

		t += choices(i, n, k) * sub_graph
		
	return t

# @test(qq,between=Cache.clear_cache)
@cache
def answer(n,k):
	ub = (n * (n - 1)) / 2 # upperbound
	lb = n - 1 # lower bound

	if k < lb or k > ub:
		return 0

	if k == lb: # cayle formula
		return int(n ** (n -2))

	if k == ub: # only 1 way, every node connected to every other
		return 1

	p = choose(ub,k) # all possible graphs w/ n nodes & k edges

	if k >= choose(lb, 2) + 1: # every way to choose a graph w/ n nodes & k edges is connected
		return p

	return p - invalid(n, k) # remove repeats and not connected graphs

def test(S,N,f, debug=False):
	for n in range(S,N+1):
		u = (n * (n-1))/2
		for k in range(n-1,u+1):
			a = f(n,k)
			if debug:
				print f.__name__, (n,k),a
				# print(chr(27) + "[2J")


def profile_theory(S,N,debug=False):
	test(S, N, qq)

def bw_steps():
	# print '-'
	Cache.debug_metrics()
	# print '-'
	Cache.clear_cache()
	Profile.debug_perf()
	print '-'

@profile(profile_theory, times=1, between=bw_steps)
# @profile(profile_theory,profile_theory2 times=10, between=bw_steps)
def profile_answer(S,N,debug=False):
	test(S, N, answer,debug)

S = 2
N = 40
profile_answer(S, N,debug=False)
print '-'
Profile.debug_perf()
print '-'
Cache.debug_metrics()
print
