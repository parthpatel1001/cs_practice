from functools import wraps
import time
import dis
from profile import profile
import random

####################
# Left & Right Shift
####################

# for i in range(0,10):
# 	x = 1 << i
# 	y = 1 * (2**i)

# 	print x==y, x , y

# for i in range(0,10):
# 	x = 512 >> i
# 	y = 512 / (2**i)

# 	print x==y, x, y


############
# Operators 
############
# & and
# ^ xor
# | for each bit, if one or both is 1
# flip all the bits
# ~1 = -2
# ~x = -1 * (x + 1)


#####################################
# If statement with bitwise operators
#####################################

def conditional(a, b , c):
	''' a is True or False, return b if a else c'''
	b_mask = (a << b.bit_length()) - a
	c_mask = (a << c.bit_length()) - a
	return (b & b_mask) + (c & ~c_mask)
	# return (b* a) + (c * (not a))

'''
implement result = a ? b : c without using if/else
-> assume a is a boolean, b and c are ints

if a is true:
	we want to return b + 0

if a is false:
	we want to return 0 + c
----------------------------
can be combined into
----------------------------

if a is true:
	(b * 1) + (c * 0)
if a is false:
	(b * 0) + (c * 1)

in python int(True) == 1, int(False) == 0

----------------------------
can be combined into
----------------------------
return (b * a) + (c * (not a))


====================
What if you can't use 'not' (!)
- bin(x) -> gives the int x in binary

Ex.
b = 11
c = 12

bin(b) = 1011 # binary repr of 11
bin(c) = 1100 # binary repr of 12

Bit wise & can give us the original number or 0:
1011 & 1111 == 1011
1011 & 0000 == 0000

But, we need a mask of the same length as the number
i.e. bin(11) == 1011, we need a mask of length 4 - 1111, (0000 if a was False)

bin(True << 4) == 10000 # (shift True 4 bits)
bin((True << 4) - 1) == 1111 # <- what we want (1 << n == 1 * (2^n)) 

bin(False << 4) == 00000
bin((False << 4) - 1) = -1 # <- fuck
bin((False << 4)) - 0) = 0000 = 0 # <-- what we want


a << b.bit_length() # shift the bool by the right number of bits
(a << b.bit_length()) - a # subtract 1 if a is true, otherwise 0 (to avoid going negative if a was False)

do the same for c

if c_mask = 101101
  ~c_mask = 010010


'''

# checks = [True, False]
# nums = [(random.randint(1, 100), random.randint(1, 100)) for i in range(1, 10)]

# for (b,c) in nums:
# 	for a in checks:
# 		expected = (a, b if a else c)
# 		result = (a, conditional(a, b, c))
# 		print 'PASSED' if expected == result else 'FAILED', (a,b,c),'Expected:', expected, 'Result:', result



'''
PASSED Expected: (True, 54) Result: (True, 54)
PASSED Expected: (False, 57) Result: (False, 57)
PASSED Expected: (True, 31) Result: (True, 31)
PASSED Expected: (False, 64) Result: (False, 64)
PASSED Expected: (True, 18) Result: (True, 18)
PASSED Expected: (False, 20) Result: (False, 20)
PASSED Expected: (True, 31) Result: (True, 31)
PASSED Expected: (False, 73) Result: (False, 73)
PASSED Expected: (True, 8) Result: (True, 8)
PASSED Expected: (False, 69) Result: (False, 69)
PASSED Expected: (True, 78) Result: (True, 78)
PASSED Expected: (False, 28) Result: (False, 28)
PASSED Expected: (True, 23) Result: (True, 23)
PASSED Expected: (False, 32) Result: (False, 32)
PASSED Expected: (True, 7) Result: (True, 7)
PASSED Expected: (False, 89) Result: (False, 89)
PASSED Expected: (True, 6) Result: (True, 6)
PASSED Expected: (False, 72) Result: (False, 72)

'''

################
# Is power of 2
################





def is_power_of_2(n):
	return (n & n - 1) == 0


def is_power_of_2_mod(m):
	n = m
	while n > 1:
		rem = n % 2
		if rem:
			return False
		n/=2
	return True

@profile
def test_bitwise(j):
	for i in range(1,j):
		is_power_of_2(i)
@profile
def  test_mod(j):
	for i in range(1,j):
		is_power_of_2_mod(i)

j = 1000000

test_mod(j)
test_bitwise(j)

# print is_power_of_2_mod(8)
# print is_power_of_2_mod(16)
# print is_power_of_2_mod(18)

# print is_power_of_2(8)
# print is_power_of_2(16)
# print is_power_of_2(18)

# print dis.dis(is_power_of_2)
# print '---------------'
# print dis.dis(is_power_of_2_mod)

#################################
# swap two variables without temp
#################################

x = 45
y = 55

y = x + y # y = 100
x = y - x # x = 55
y = y - x # y = 45

x,y

#############################################
# An array of integers of size n-1, 
# all the elements are form [1,n]. 
# Find the missing number. 
# You can read only one bit in one operation, 
# ie, to read A[i], 
# you need to perform log(A[i]) operations.
#############################################

# size = 5
# [3,1,2,6,4]

# 1 -> 001
# 2 -> 010
# 3 -> 011
# 4 -> 100
# 5 -> 101
# 6 -> 110

def find_missing(n):
	mask = 1 << len(n) + 1
	for i in n:
		mask |= (1 << (i - 1))
	missing = 1
	l = mask
	while mask > 0:
		if not(mask & 1):
			return missing
		else:
			mask = mask >> 1
			missing+=1
	raise KeyError('No missing %s %s' % (n, bin(mask)))

def find_missing_xor(n):
	j = len(n) + 1
	mask = 0 ^ j
	for i in n:
		j-=1
		mask ^= j
		mask ^= i
	return mask

def get_missing_array(j):
	items = [i for i in range(1,j)]
	random.shuffle(items)
	items.pop()
	return items

@profile
def test_missing(j,k):
	for i in range(1, j):
		find_missing(get_missing_array(k))

@profile
def test_missing_xor(j,k):
	for i in range(1, j):
		find_missing_xor(get_missing_array(k))
j = 100000
k = 10
test_missing(j,k)
test_missing_xor(j,k)
# for i in range(1,10):
# 	i = get_missing_array(6)
# 	print i, find_missing(i), '|',find_missing_xor(i)




