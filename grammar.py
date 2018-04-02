#!/bin/env python

# dear teammates: i apologize in advance for this terrible code

import pdb
import collections

# rule format is (parent, child1, child2, etc)
# where parent/childx is of the form (symbol, parameters)
# symbol is just some string representing the type of phrase, eg "NP"
# parameters is a string of characters, where the inclusion of a character indicates that parameter is true and the exclusion indicates that it is false
# unmentioned parameters must have the same value for all terms in that rule
# eg (("A", "a"), ("B", "b"), ("C, "")) can derive
# (("A", "a"), ("B", "b"), ("C, "")) and
# (("A", "ac"), ("B", "bc"), ("C, "c")) since "c" is unmentioned so it can take either value as long as it's consistent
# but not
# (("A", "ac"), ("B", "b"), ("C, "")) because the value of "c" is not consistent
# or (("A", "a"), ("B", ""), ("C, "")) because the value of "b" does not match the rule specifier
# ask luke for more clarification

# parameters:
# .: null complementizer
# ?: inflector moved to complementizer
# m: null inflector
# a: no subject

# TODO: add tense parameters for V/VP

# notes:
# IP has form DP I VP, I' has form I VP

rules = [
	(("IP", ""), ("DP", "S"), ("I'", "S")),
	(("IP", ""), ("DP", "P"), ("I'", "P")),

	(("S", ""), ("CP", "."), (".", "")),
	(("S", ""), ("CP", "?"), ("?", "")),

	(("CP", "."), ("IP", "")), # null complementizer

	(("CP", ""), ("IP", "")), # null complementizer
	(("CP", ""), ("C", "i"), ("IP", "")),

	#(("CP", "?"), ("I", "v"), ("IP", "m")), # I to C movement
	#(("IP", "m"), ("DP", ""), ("I'", "m")),
	#(("I'", "m"), ("VP", "")), # move/missing inflector

	# null determiner
	(("DP", ""), ("NAME", "0")),

	# PP adjuncts
	(("NP", ""), ("NP", ""), ("PP", "", 0)),

	# CP adjunct
	(("NP", ""), ("NP", ""), ("CP", "a")),
	(("CP", "a"), ("C", "i"), ("IP", "a")),
	(("IP", "a"), ("I'", "")), # IP with no subject

	# head complements
	# no complements
	(("NP", ""), ("N", "0")),
	(("VP", ""), ("V", "0")),
	((".", ""), (".", "0")),
	(("?", ""), ("?", "0")),
	# VP complements
	#(("I'", ""), ("I", "v"), ("VP", "")),
	# DP complements
	(("VP", ""), ("V", "d"), ("DP", "", 0)),
	(("PP", ""), ("P", "d"), ("DP", "")),
	# NP complements
	(("DP", ""), ("D", "n"), ("NP", "")),
	# CP complements
	(("VP", ""), ("V", "c"), ("CP", "", 0)),

	# inflection rules
	# I' parameters:
	# V: voice
	# T: progressive aspect
	# A: perfect aspect
	# M: modality
	(("VP", "P"), ("VP", "")),

	(("I'", "R"), ("VP", "R")), # root
	(("I'", "G"), ("VP", "G")), # progressive
	(("I'", "N"), ("VP", "N")), # perfect nonprogressive

	(("I'", "G"), ("I", "$_"), ("VP", "N")), # passive progressive, eg being known
	(("I'", "N"), ("I", "%_"), ("VP", "N")), # perfect nonprogressive, eg been known
	(("I'", "N"), ("I", "%_"), ("VP", "G")), # perfect nonprogressive, eg been knowing
	(("I'", "R"), ("I", "*_"), ("VP", "N")), # eg be known
	(("I'", "R"), ("I", "*_"), ("VP", "G")), # eg be knowing

	(("I'", "P"), ("VP", "P")), # active plural, eg know
	(("I'", "S"), ("VP", "S")), # active singular, eg knows
	(("I'", "P"), ("VP", "PT")), # past plural, eg knew
	(("I'", "S"), ("VP", "ST")), # past singular, eg knew
	(("I'", "P"), ("I", "DP_"), ("VP", "R")), # active plural, eg do know
	(("I'", "S"), ("I", "DS_"), ("VP", "R")), # active singular, eg does know;
	(("I'", "P"), ("I", "VP_"), ("VP", "N")), # passive plural, eg are known
	(("I'", "S"), ("I", "VS_"), ("VP", "N")), # passive singular, eg is known

	(("I'", "S"), ("I", "VS_"), ("I'", "G")), # continuous singular, eg is knowing
	(("I'", "P"), ("I", "VP_"), ("I'", "G")), # continuous plural, eg are knowing

	#(("I'", "T"), ("I", "H"), ("I'", "N")), # have known
]

# vocab format is (word, part of speech, selection parameters, other parameters)
# selection parameters do not get passed up the chain
# and are only used to select complements
# other parameters get passed up chain
vocabulary = [
	("Arthur", "NAME", "0"),
	("Guinevere", "NAME", "0"),
	("Sir Lancelot", "NAME", "0"),
	("Sir Bedevere", "NAME", "0"),
	("Zoot", "NAME", "0"),
	("Patsy", "NAME", "0"),
	("Uther Pendragon", "NAME", "0"),
	("the", "D", "n", "S"),
	("the", "D", "n", "P"),
	("king", "N", "0"),
	#("horse", "N", "0", "S"),
	#("snakes", "N", "0", "P"),
	("near", "P", "d"),
	("castle", "N", "0", "S"),
	("defeater", "N", "0", "S"),
	("servant", "N", "0", "S"),
	("corner", "N", "0", "S"),
	("land", "N", "0", "S"),
	("quest", "N", "0", "S"),
	("chalice", "N", "0", "S"),
	("master", "N", "0", "S"),
	("horse", "N", "0", "S"),
	("fruit", "N", "0", "S"),
	("swallow", "N", "0", "S"),
	("sun", "N", "0", "S"),
	("winter", "N", "0", "S"),
	("coconut", "N", "0", "S"),
	("pound", "N", "0", "S"),
	("husk", "N", "0", "S"),
	("home", "N", "0", "S"),
	("weight", "N", "0", "S"),
	("story", "N", "0", "S"),
	("sovereign", "N", "0", "S"),
	#("suggest", "V", "dc"),
	("that", "C", "i"),

	("of", "P", "d"),
	("of", "P", "name"),
	("above", "P", "d"),
	("above", "P", "name"),
	("across", "P", "d"),
	("at", "P", "d"),
	("below", "P", "d"),
	("below", "P", "name"),
	("by", "P", "d"),
	("by", "P", "name"),
	("for", "P", "d"),
	("for", "P", "name"),
	("from", "P", "d"),
	("from", "P", "name"),
	("into", "P", "d"),
	("near", "P", "d"),
	("near", "P", "name"),
	("on", "P", "d"),
	("over", "P", "d"),
	("through", "P", "d"),
	("with", "P", "d"),
	("with", "P", "name"),

	("a", "D", "n", "S"),
	("another", "D", "n", "S"),
	("any", "D", "n", "S"),
	("any", "D", "n", "P"),
	("each", "D", "n", "S"),
	("every", "D", "n", "S"),
	("no", "D", "n", "P"),
	("that", "D", "n", "S"),
	("this", "D", "n", "S"),


	# wh words
	("what", "Q", "0"),
	("who", "Q", "0"),
	("where", "Q", "0"),
	#("why", "Q", "0"),

	("cat", "N", "0"),
	("dog", "N", "0"),
	("bunny", "N", "0"),
	#("run", "V", "0"),
	#("eat", "V", "0d"),
	#("give", "V", "0"), # will handle indirect objects later
	#("does", "I", "v"),
	#("did", "I", "v"),
	#("will", "I", "v"),

	(".", ".", "0"),
	("!", ".", "0"),
	("?", "?", "0"),

	# note: don't currently have rules / parameters to handle below words
	# inflectors
	("do", "I", "_", "DP"),
	("does", "I", "_", "DS"),

	("is", "I", "_", "VS"),
	("was", "I", "_", "VS"),

	("are", "I", "_", "VP"),
	("were", "I", "_", "VP"),

	("be", "I", "_", "*"),
	("been", "I", "_", "%"),
	("being", "I", "_", "$"),

	("can", "I", "_", ""),

	# perfect
	("had", "I", "_", "HT"),
	("has", "I", "_", "HS"),
	("have", "I", "_", "HP"),

	# modal inflectors
	("may", "I", "_", "M"),
	("might", "I", "_", "M"),
	("must", "I", "_", "M"),
	("shall", "I", "_", "M"),
	("should", "I", "_", "M"),
	("would", "I", "_", "M"),
	("could", "I", "_", "M"),
	("will", "I", "_", "M"),

	# verbs
	# R: root
	# S: singular present
	# P: past
	# G: progressive
	# N: perfect nonprogressive
	("knew", "V", "0dc", "PT"),
	("knew", "V", "0dc", "ST"),
	("know", "V", "0dc", "P"),
	("know", "V", "0dc", "R"),
	("knowing", "V", "0dc", "G"),
	("known", "V", "0", "N"),
	("knows", "V", "0dc", "S"),
]

# types of complements each head can have
selection_rules = {
	"V": "0dcp",
	"I": "_",
	"N": "0",
	"D": "n",
	"P": "d",
	"NAME": "0",
	".": "0",
	"?": "0",
}

vocab_parameters = collections.defaultdict(str, {
	"V": "RSPGNT",
	"I": "DPSV*%$HTM",
	"N": "SP",
	"D": "SP",
})

carried_parameters = set(char for char in "m.?RSPGNTS")

def enumerate_parameters(parameters):
	if len(parameters) == 0:
		return [""]
	return [
		p + suffix
		for p in enumerate_parameters(parameters[1:])
		for suffix in (parameters[0], "")
	]

def gen_tag(symbol, parameters):
	p = "".join(sorted(set(c for c in parameters)))
	return "{}_({})".format(symbol, p)

def gen_rules(rule):
	used_parameters = {
		char
		for r in rule
		for char in r[1]
	}
	remaining_parameters = "".join(carried_parameters - used_parameters)
	return [
		(
			gen_tag(rule[0][0], parameters + rule[0][1]),
			[
				gen_tag(r[0], ("" if len(r) > 2 and r[2] == 0 else parameters) + r[1])
				for r in rule[1:]
			]
		)
		for parameters in enumerate_parameters(remaining_parameters)
	]

def gen_vocab_rule(word, symbol, selection_parameters, parameters=""):
	return (gen_tag(symbol, "".join(sorted(c for c in selection_parameters + parameters))), (word,))

def gen_grammar(rules):
	grammar = [
		static_rule
		for rule in rules
		for static_rule in gen_rules(rule)
	] + [
		gen_vocab_rule(*word)
		for word in vocabulary
	] + [
		("START", "S"),
		("S", ("S_()",)),
	] + [
		(gen_tag(pos, p + vp), (gen_tag(pos, parameters + vp),))
		for pos, possible_parameters in selection_rules.items()
		for parameters in enumerate_parameters(possible_parameters)
		for p in parameters
		for vp in enumerate_parameters(vocab_parameters[pos])
		if len(parameters) > 1
	]

	# filter out unusued rules that can't derive anything
	#while False:
	while True:
		initial_length = len(grammar)
		# terms are invalid if cannot derive anything
		valid = {
			rule[0]
			for rule in grammar
		} | {
			word[0]
			for word in vocabulary
		}
		grammar = [
			rule
			for rule in grammar
			if all(
				tag in valid
				for tag in rule[1]
			)
		]

		# if didn't remove anything we're done
		if len(grammar) == initial_length:
			break

	return grammar

def to_string(grammar):
	return "\n".join(
		"\t".join((
			"1",
			rule[0],
			" ".join(rule[1]),
		)) for rule in grammar
	)

print(to_string(gen_grammar(rules)))

#pdb.set_trace()

