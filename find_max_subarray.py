def find_max_crossing_subarray(a, low, mid, high):
	left_sum = None
	total = 0
	max_left = None
	
	for i in range(mid, -1, -1):
		total += a[i]
		if total > left_sum:
			left_sum = total
			max_left = i

	right_sum = None
	total = 0
	max_right = None
	
	for j in range(mid + 1, high +1):
		total += a[j]	
		if total > right_sum:
			right_sum = total
			max_right = j

	return (max_left, max_right, left_sum + right_sum)

def find_maximum_subarray(a, low, high):
		if low == high:
			return (low, high, a[low])
		else:
			mid = (low + high) / 2
			left_low, left_high, left_sum    = find_maximum_subarray(a, low, mid)
			right_low, right_high, right_sum = find_maximum_subarray(a, mid + 1, high)
			cross_low, cross_high, cross_sum = find_max_crossing_subarray(a, low, mid, high)
			if left_sum >= right_sum and left_sum >= cross_sum:
				return (left_low, left_high, left_sum)
			elif right_sum >= left_sum and right_sum >= cross_sum:
				return (right_low, right_high, right_sum)
			else:
				return (cross_low, cross_high, cross_sum)

x = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]

print find_maximum_subarray(x, 0, len(x) - 1)