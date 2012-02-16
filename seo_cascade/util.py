def unique_by(seq, idfun=None):
	"""Return a unique list, in order, with an optional property filter.

	>>> unique_by([1, 2, 2, 3])
	[1, 2, 3]
	>>> unique_by([{'prop': 1}, {'prop': 2}, {'prop': 2}, {'prop': 3}], lambda x: x.prop)
	[{'prop': 1}, {'prop': 2}, {'prop': 3}]
	"""
	# order preserving
	if idfun is None:
		def idfun(x):
			return x
	seen = []
	result = []
	for item in seq:
		marker = idfun(item)
		# in old Python versions:
		# if seen.has_key(marker)
		# but in new ones:
		if marker in seen:
			continue
		seen.append(marker)
		result.append(item)
	return result


def first_of(iterable, default=None):
	"""Return the first item of iterable argument,
	or None if the argument is not iterable"""
	if iterable:
		for item in iterable:
			return item
	return default


def red(x):
	print ""
	print '\033[1;31m@-->%r\033[1;m' % x
	print '\033[1;37m-------------------\033[1;m'
