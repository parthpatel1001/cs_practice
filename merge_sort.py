def merge_sort(items):
	if len(items) == 1:
		return items
	l = len(items)
	m = l/2
	left = merge_sort(items[0:m])
	right = merge_sort(items[m:])
	llen = len(left)
	rlen = len(right)
	i = j = k = 0

	while i < llen and j < rlen:
		if left[i] < right[j]:
			items[k] = left[i]
			i+=1
		else:
			items[k] = right[j]
			j+=1
		k+=1

	return items[0:k] + left[i:] if i < llen else [] + right[j:] if j < rlen else []


print merge_sort([9,8,7,6,5,1,2,3,4])