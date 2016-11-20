import time
from functools import wraps
import traceback

class Experiment(object):
	_theories = []
	_experiments = {}

	def __init__(self, *theories, **kwargs):
		Experiment._theories += list(theories)
		self.theories = Experiment._theories
		self.experiments = Experiment._experiments

	def __enter__(self):
		return self

	def __call__(self, fn):
		@wraps(fn)
		def experiment(*args, **kwargs):
			expected, took = self._time(fn, *args,  **kwargs)
			self.experiments[fn] = {'pass':None, 'took': took, 'res':expected}


			for theory in self.theories:
				res, took = self._time(theory, *args, **kwargs)
				self.experiments[theory] = {'pass':expected == res, 'took': took, 'res':res}
			# print self.experiments
			return expected
		return experiment

	def __exit__(self, exception, value, trace):
		if exception:
			traceback.print_exception(exception, value, trace)
			return False
		return True

	def __del__(self):
		pass

	def _time(self, fn, *args, **kwargs):
		start = int(round(time.time() * 1000))
		res = fn(*args,**kwargs)
		end = int(round(time.time() * 1000))
		return res, end - start

	def results(self, debug=False):
		if debug:
			for fn, result in self.experiments.iteritems():
				print fn.__name__, result
		return self.experiments


def test_function_control(a,b,c):
	time.sleep(.25)
	return a / b / c

def test_function_one(a,b,c):
	time.sleep(1)
	return a + b + c


def test_function_two(a,b,c):
	time.sleep(.5)
	return a * b * c

@Experiment(test_function_one, test_function_two, test_function_control)
def test_function_three(a,b,c):
	time.sleep(.25)
	return a / b / c



with Experiment() as Exp:
	
	a = 10
	b = 5
	c = 1
	test_function_three(a,b,c)
	Exp.results(debug=True)