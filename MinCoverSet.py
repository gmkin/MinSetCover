import sys, time

global sets							# encompasses all sets
global FULLSET						# set we are trying to achieve
global maxNum						# max element in lists
global best							# min cover set
global dp			# dp dict map input -> array for answer


def attemptCoverSet(setCover, startPos, depth, data):
	global best
	global sets
	global FULLSET

	if depth >= len(best):	# or len(data) >= len(best):
		return						# self-purge, too long
	if setCover == FULLSET:			# we found a better solution
		best = data.copy()
		# print_sets(best)
		return

	for i in range(startPos, len(sets)):
		rep = setCover | sets[i]
		if rep == setCover:
			continue
		data.append(sets[i])
		attemptCoverSet(rep, i + 1, depth + 1, data)
		data.remove((sets[i]))


def attemptCoverSet2(setCover, startPos, depth, data):
	global best
	global sets
	global FULLSET
	global dp

	if depth >= len(best):
		return None					# self-purge, too long
	if setCover == FULLSET:			# we found a better solution
		best = data.copy()
		print_sets(best)
		return []

	if setCover in dp:
		if dp[setCover] is None:
			pass
		elif len(dp[setCover]) + len(data) < len(best):
			# print("DP hit", dp[setCover], bin(setCover))
			temp = setCover
			for k in dp[setCover]:
				temp |= k
			if temp == FULLSET:
				best = data.copy() + dp[setCover]
				print_sets(best)
			return dp[setCover]

	run_best = None
	this_set = sets.copy()
	this_set.sort(key=lambda x: bin(x & ~setCover).count("1"), reverse=True)

	for i in range(startPos, len(this_set)):
		loop_best = this_set[i]
		rep = setCover | loop_best
		if rep == setCover:
			continue
		data.append(loop_best)
		rt = attemptCoverSet2(rep, i + 1, depth + 1, data)
		data.remove(loop_best)

		if run_best is None:
			run_best = [loop_best] if rt is None else [loop_best] + rt
		elif rt is not None and len(rt) + 1 < len(run_best):
			run_best = [loop_best] + rt
		if len(run_best) == 1:		# cannot get any better
			break
	dp[setCover] = run_best
	return run_best


def greedy(rt_set, cover):
	global sets
	global FULLSET

	while cover != FULLSET:
		sets.sort(key=lambda x: bin(x & ~cover).count("1"), reverse=True)
		cover |= sets[0]
		rt_set.append(sets[0])
	return rt_set


def print_sets(sets):
	if not sets:
		return
	print("-------------------------------------")
	for k in sets:
		print('{:>41}+{}'.format(bin(k)[2:], bin(k & ~setCover).count("1")))


def print_asNum(sets):
	global maxNum

	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	for k in sets:		# converts num back into human readable representations
		for ele in range(0, maxNum):
			if ((1 << ele) | k) == k:
				print('{:3}'.format(ele + 1), end=' ')
		print()


if __name__ == '__main__':
	global sets
	global FULLSET
	global maxNum
	global best
	global dp

	start = time.time()

	dp = {}
	singles = None					# if there exists such a singularity for element
	lineNo = 0						# only used to obtain first 2 num
	for currLine in open(sys.argv[1], "r"):
		lineNo += 1
		if lineNo == 1:
			maxNum = int(currLine)
			FULLSET = (1 << maxNum) - 1
			singles = [None] * maxNum
			sets = []
			continue
		if lineNo == 2:				# ignore as we read until EOF
			continue
		setLine = 0					# map set -> int
		for num in currLine.split(" "):
			if num == '\n':			# end of line
				break
			setLine |= 1 << (int(num) - 1)

		isIn = False				# setLine is not in sets
		for i in range(len(sets) - 1, 0, -1):
			set = sets[i]
			newSet = setLine | set
			if newSet == setLine:	# set is subset of newSet
				sets.remove(set)
			if newSet == set:		# newSet is subset of set
				isIn = True			# discard newSet
				break
		if not isIn:
			sets.append(setLine)	# add to possible sets
			for ele in range(0, maxNum):
				if ((1 << ele) | setLine) == setLine:
					singles[ele] = setLine if singles[ele] is None else 0

	setCover = 0					# Current cover for set
	sets.sort(key=lambda x: bin(x & ~setCover).count("1"), reverse=True)
	minSetCover = []
	for ele in singles:
		if ele == 0:
			continue
		if ele is None:
			print("NO SET COVER POSSIBLE, MISSING A ELEMENT")
			exit(1)
		cover = setCover | ele
		if cover != setCover:
			setCover = cover
			minSetCover.append(ele)
			sets.remove(ele)

	if setCover == FULLSET:
		print_asNum(minSetCover)
		exit(0)

	best = greedy(minSetCover.copy(), setCover)
	attemptCoverSet2(setCover, 0, len(minSetCover), minSetCover)

	print(setCover)
	print_asNum(dp[setCover]+minSetCover)

	print_asNum(best)				# one such solution
	print(time.time() - start)
