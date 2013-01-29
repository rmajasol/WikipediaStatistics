import global_var2
test_mode = False
print test_mode  # False


def f2():
	print test_mode


def f1(test):
	global test_mode
	test_mode = test

	f2()


f1(True)  # True

global_var2.run(test_mode)
