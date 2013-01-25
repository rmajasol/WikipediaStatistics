myString = "Hello there !bob@"
mySubString = myString[myString.find("!") + 1:myString.find("@")]
print mySubString

s = "log-20120616.gz"
LOG_MONTH = s[8:10]
print LOG_MONTH


def print_some(cad):
	print cad
