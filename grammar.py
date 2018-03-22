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
rules = [
	(("IP", ""), ("NP", ""), ("I'", "")),
	(("I'", ""), ("I", ""), ("VP", "")),
	(("NP", ""), ("N", "")),
	(("VP", ""), ("V", "")),

	(("S", ""), ("CP", "0"), (".", "")),
	(("S", ""), ("CP", "?"), ("?", "")),

	(("CP", "0"), ("IP", "")), # null complementizer

	(("CP", "?"), ("I", ""), ("IP", "0")), # I to C movement
	(("IP", "0"), ("NP", ""), ("I'", "0")),
	(("I'", "0"), ("VP", "")), # null inflector
]

# vocab format is (word, part of speech, parameters)
vocabulary = [
	("cat", "N", ""),
	("dog", "N", ""),
	("bunny", "N", ""),
	("run", "V", ""),
	#("eat", "V", ""), # will handle transitives later
	#("give", "V", ""), # will handle indirect objects later
	("does", "I", ""),
	("did", "I", ""),
	("will", "I", ""),

	(".", ".", ""),
	("!", ".", ""),
	("?", "?", ""),
]

all_parameters = set(char for char in "0.?")

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
	remaining_parameters = "".join(all_parameters - used_parameters)
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

def gen_vocab_rule(word, obj):
	return (gen_tag(*obj), (word,))

def gen_grammar(rules):
	grammar = [
		static_rule
		for rule in rules
		for static_rule in gen_rules(rule)
	] + [
		gen_vocab_rule(word, (symbol, parameters))
		for word, symbol, parameters in vocabulary
	] + [
		("START", "S"),
		("S", ("S_()",)),
	]

	# filter out unusued rules that can't derive anything
	while True:
		initial_length = len(grammar)
		# terms are invalid if cannot derive anything
		valid = {
			rule[0]
			for rule in grammar
		} | {
			word
			for word, symbol, parameters in vocabulary
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

