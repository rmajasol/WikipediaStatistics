#!/usr/bin/python

from optparse import OptionParser


# http://www.saltycrane.com/blog/2009/09/python-optparse-example/
# http://docs.python.org/2/library/optparse.html#handling-boolean-flag-options
# http://docs.python.org/2/library/optparse.html#standard-option-actions
def main():
	parser = OptionParser()
	parser.add_option('-t', '--test',
		action="store_true",
		dest="test",
		default=False,
		help='Runs in test mode')
	parser.add_option('-m', '--manual',
		nargs=2,
		# action="store_true",
		dest="manual",
		default=False,
		help='Manually process a certain volume of logs between 2 dates.\n' + \
			'e.g. option_parser.py -m 20130101 20130327 -> ' + \
			'This will process all logfiles between 1st Jan 2013 and 27th Mar 2013')

	(opts, args) = parser.parse_args()

	if opts.test:
		print "con test"
	else:
		print "sin test"

	if opts.manual:
		print "con modo manual entre " + opts.manual[0] + " y " + opts.manual[1]
		print type(opts.manual[0])
	else:
		print "sin modo manual"

	print opts
	print args

if __name__ == '__main__':
	main()
