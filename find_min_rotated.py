def find_min(nums):
	rpos = len(nums) / 2
	left = nums[0]
	right = nums[rpos]

	if left < right:
		return find_min(nums[rpos:])

	if rpos == 1:
		return right

	return find_min(nums[0:rpos + 1])

def find_min_nr(nums):
	nlen = len(nums)
	lpos = 0
	
	while True:
		rpos = (nlen / 2) + lpos
		left = nums[lpos]
		right = nums[rpos]

		if left < right:
			lpos = rpos
			nlen -= rpos
			continue

		if rpos == 1:
			return right

		nlen = rpos + 1

def test(nums):
	res = find_min_nr(nums)
	expected = min(nums)
	print nums, res, 'expected', expected, res == expected


test([5,6,7,8,9,1,2,3,4])
test([6,7,8,9,1,2,3,4,5])