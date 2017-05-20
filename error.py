import os

def c():
	os.system('clear')

def error(errtype, msg):
	raise errtype('💔  {}'.format(msg))