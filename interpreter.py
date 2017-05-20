import functools
import operator

from error import *
import parse

stos_zła = [{
	'+': operator.add,
	'-': operator.sub,
	'*': operator.mul,
	'/': operator.truediv,
	'√': lambda x: x**0.5,
},  {}]

class Builtins:
	def define(name, value):
		if not name.token[0] == 'symbol':
			error(NameError, 'CANNOT ASSIGN VALUE TO {}'.format(name.token[0]))
		stos_zła[-1][name.token[1]] = evaluate(value)
		return stos_zła[-1][name.token[1]]

	def dalamb(arguments, *expressions):
		return parse.Node(('func',(vec_data(arguments),expressions,),'NONEXISTENT','NONEXISTENT',))

macroos = {
	'def': Builtins.define,
	'lambda': Builtins.dalamb,
	'λ': Builtins.dalamb
}

def symbol_search(symbol):
	i = len(stos_zła) - 1
	while i >= 0:
		try:
			return stos_zła[i][symbol[1]]
		except:
			i -= 1

	error(NameError, 'NO SACH SYMBOL at line {} column {}'.format(symbol[2], symbol[3]))


def number_eval(node):
	return float(node.token[1])


def string_eval(node):
	return node.token[1][1:-1]

def symbol_eval(node):
	return symbol_search(node.token)


def func_eval(function,values):
	global stos_zła
	_, (arguments, expressions), _, _ = function.token
	if not len(arguments) == len(values):
		error(TypeError,'zła ARYJSKOŚĆ')
	stos_zła.append({a.token[1]: evaluate(v) for a, v in zip(arguments, values)})

	n = parse.Node(('','','','',))
	for e in expressions:
		n.adopt(e)
	res = run(n)
	stos_zła.pop()
	return res


def apply_eval(node):
	if node.kids[0].token[0] == '(':
		node.kids[0] = evaluate(node.kids[0])


	if node.kids[0].token[0] == 'func':
		return func_eval(node.kids[0], node.kids[1:])
	try:
		s = macroos[node.kids[0].token[1]]
		args = node.kids[1:]
	except:
		s = symbol_search(node.kids[0].token)
		args = [evaluate(e) for e in node.kids[1:]]
	try:
		return s(*args)
	except TypeError:
		error(TypeError, '{}: experiencing unexpected error, please try again'.format(node.kids))

def vec_eval(node):
	return [evaluate(e) for e in node.kids]

def vec_data(node):
	return node.kids

map_evil = {
	'(': apply_eval,
	'[': vec_eval,
	# TODO
	'{': None,
	'string': string_eval,
	'number': number_eval,
	'symbol': symbol_eval,
	'func': func_eval
}

def evaluate(node):
	return map_evil[node.token[0]](node)

def run(tree):
		return [str(evaluate(kid)) for kid in tree.kids][-1]
