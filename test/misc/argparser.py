#!/usr/bin/python

from argparse import ArgumentParser


# http://www.saltycrane.com/blog/2009/09/python-optparse-example/
# http://docs.python.org/2/library/optparse.html#handling-boolean-flag-options
# http://docs.python.org/2/library/optparse.html#standard-option-actions
def main():
	parser = ArgumentParser()
	parser.add_argument('-t', '--test',
		action="store_true",
		dest="test",
		default=False,
		help='Runs in test mode')
	parser.add_argument('-m', '--manual',
		nargs=2,
		# http://argparse.googlecode.com/svn/trunk/doc/add_argument.html#metavar
		metavar=('INIT_DATE', 'FINAL_DATE'),
		# action="store_true",
		dest="manual",
		default=False,
		help='Manually process a certain volume of logs between 2 dates.\n' + \
			'e.g. option_parser.py -m 20130101 20130327 -> ' + \
			'This will process all logfiles between 1st Jan 2013 and 27th Mar 2013')

	args = parser.parse_args()

	if args.test:
		print "con test"
	else:
		print "sin test"

	if args.manual:
		print "con modo manual entre " + args.manual[0] + " y " + args.manual[1]
		print type(args.manual[0])
	else:
		print "sin modo manual"

	print args

if __name__ == '__main__':
	main()
