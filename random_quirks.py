def my_function():
	try:
		print 'returning'
		return 'returned something'
	except Exception as e:
		print 'caught an exception e'
	finally:
		print 'finally did something'

print my_function()