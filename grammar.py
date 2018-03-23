#!/bin/env python

# dear teammates: i apologize in advance for this terrible code

import pdb

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
	(("IP", ""), ("DP", ""), ("I'", "")),

	(("S", ""), ("CP", "."), (".", "")),
	(("S", ""), ("CP", "?"), ("?", "")),

	(("CP", "."), ("IP", "")), # null complementizer

	(("CP", ""), ("IP", "")), # null complementizer
	(("CP", ""), ("C", "i"), ("IP", "")),

	(("CP", "?"), ("I", "v"), ("IP", "m")), # I to C movement
	(("IP", "m"), ("DP", ""), ("I'", "m")),
	(("I'", "m"), ("VP", "")), # move/missing inflector

	# null determiner
	(("DP", ""), ("NAME", "0")),

	# PP adjuncts
	(("NP", ""), ("NP", ""), ("PP", "")),

	# CP adjunct
	(("NP", ""), ("NP", ""), ("CP", "a")),
	(("CP", "a"), ("C", "i"), ("IP", "a")),
	(("IP", "a"), ("I", "v"), ("VP", "")), # IP with no subject

	# head complements
	# no complements
	(("NP", ""), ("N", "0")),
	(("VP", ""), ("V", "0")),
	((".", ""), (".", "0")),
	(("?", ""), ("?", "0")),
	# VP complements
	(("I'", ""), ("I", "v"), ("VP", "")),
	# DP complements
	(("VP", ""), ("V", "d"), ("DP", "")),
	(("PP", ""), ("P", "d"), ("DP", "")),
	# NP complements
	(("DP", ""), ("D", "n"), ("NP", "")),
	# CP complements
	(("VP", ""), ("V", "c"), ("CP", "")),
]

# vocab format is (word, part of speech, selection parameters, other parameters)
# selection parameters do not get passed up the chain
# and are only used to select complements
# other parameters get passed up chain
vocabulary = [
	("Arthur", "NAME", "0"),
	("the", "D", "n"),
	("king", "N", "0"),
	("horse", "N", "0"),
	("near", "P", "d"),
	("castle", "N", "0"),
	("suggest", "V", "dc"),
	("that", "C", "i"),
	("of", "P", "d"),

	# wh words
	("what", "Q", "0"),
	("who", "Q", "0"),
	("where", "Q", "0"),
	#("why", "Q", "0"),

	("cat", "N", "0"),
	("dog", "N", "0"),
	("bunny", "N", "0"),
	("run", "V", "0"),
	("eat", "V", "0d"),
	#("give", "V", "0"), # will handle indirect objects later
	("does", "I", "v"),
	("did", "I", "v"),
	("will", "I", "v"),

	(".", ".", "0"),
	("!", ".", "0"),
	("?", "?", "0"),

	# note: don't currently have rules / parameters to handle below words
	# inflectors
	("does", "I", "", ""),
	("will", "I", "", ""),

	("is", "I", "", ""),
	("was", "I", "", ""),

	("are", "I", "", ""),
	("were", "I", "", ""),

	("be", "I", "", ""),
	("been", "I", "", ""),
	("being", "I", "", ""),
	("can", "I", "", ""),
	("could", "I", "", ""),
	("do", "I", "", ""),
	("had", "I", "", ""),
	("has", "I", "", ""),
	("have", "I", "", ""),
	("having", "I", "", ""),

	("may", "I", "", ""),
	("might", "I", "", ""),
	("must", "I", "", ""),
	("shall", "I", "", ""),
	("should", "I", "", ""),
	("would", "I", "", ""),

	# verbs
	("knew", "V", "dc", ""),
	("know", "V", "dc", ""),
	("knowing", "V", "dc", ""),
	("known", "V", "dc", ""),
	("knows", "V", "dc", ""),
]

# types of complements each head can have
selection_rules = {
	"V": "0dcp",
	"I": "v",
	"N": "0",
	"D": "n",
	"P": "d",
	"NAME": "0",
	".": "0",
	"?": "0",
}

carried_parameters = set(char for char in "m.?")

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
		for symbol, parameters in rule
		for char in parameters
	}
	remaining_parameters = "".join(carried_parameters - used_parameters)
	return [
		(
			gen_tag(rule[0][0], parameters + rule[0][1]),
			[
				gen_tag(r[0], parameters + r[1])
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
		(gen_tag(pos, p), (gen_tag(pos, parameters),))
		for pos, possible_parameters in selection_rules.items()
		for parameters in enumerate_parameters(possible_parameters)
		for p in parameters
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

