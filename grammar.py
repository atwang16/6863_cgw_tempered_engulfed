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
	(("IP", ""), ("DP", "S"), ("I'", "S")),  # singular
	(("IP", ""), ("DP", "P"), ("I'", "P")),  # plural

	# imperative
	#(("S", ""), ("VP", "R")),

	(("S", ""), ("CP", "."), (".", "")),
	(("S", ""), ("CP", "?"), ("?", "")),

	(("CP", "."), ("IP", "")), # null complementizer (forced)

	(("CP", ""), ("IP", "")), # null complementizer
	(("CP", ""), ("C", "i"), ("IP", "")),

	#(("CP", "?"), ("I", "v"), ("IP", "m")), # I to C movement
	#(("IP", "m"), ("DP", ""), ("I'", "m")),
	#(("I'", "m"), ("VP", "")), # move/missing inflector

	# null determiner
	(("DP", ""), ("NAME", "0")),
	(("DP", ""), ("Pn", "0")),

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
	(("VP", ""), ("V", "d"), ("DP", "S", 0)),
	(("VP", ""), ("V", "d"), ("DP", "P", 0)),
	(("PP", ""), ("P", "d"), ("DP", "P")),
	(("PP", ""), ("P", "d"), ("DP", "S")),
	# NP complements
	(("DP", ""), ("D", "n"), ("NP", "")),
	# CP complements
	(("VP", ""), ("V", "c"), ("CP", "", 0)),
	# AP complements
	(("VP", ""), ("V", "a"), ("AP", "", 0)),
    # PP complements
    (("VP", ""), ("V", "p"), ("PP", "", 0)),

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

	(("I'", "R"), ("I", "HB_"), ("I'", "N")), # have known

	(("I'", "S"), ("I", "M_"), ("I'", "R")), # modality, eg should know
	(("I'", "P"), ("I", "M_"), ("I'", "R")), # modality, eg should know

	# verb as subject
	(("DP", "S"), ("VP", "G")),

	# adjectives
	(("AP", ""), ("A", "_")),
	(("DP", ""), ("D", "n"), ("AP", "", 0), ("NP", "")),

	# adverbs
	(("AdvP", ""), ("Adv", "0")),
    #(("VP", ""), ("VP", ""), ("AdvP", "", 0)),
    #(("VP", ""), ("AdvP", "", 0), ("VP", "")),	

    # numbers
    (("DP", ""), ("D", "n"), ("Num", ""), ("AP", "", 0), ("NP", "")),
    (("DP", ""), ("D", "n"), ("Num", ""), ("NP", "")),
    (("DP", ""), ("Num", ""), ("NP", "")),
    (("DP", ""), ("Num", ""), ("AP", "", 0), ("NP", "")),

    # pause
    (("DP", ""), ("DP", ""), ("Pause_,", "", 0), ("DP", "")),

	# coordinating conjunctions
	(("NP", "P"), ("NP", "P", 0), ("CC", "0A", 0), ("NP", "S", 0)),
	(("NP", "P"), ("NP", "S", 0), ("CC", "0A", 0), ("NP", "S", 0)),
	(("NP", "P"), ("NP", "P", 0), ("CC", "0A", 0), ("NP", "P", 0)),
	(("NP", "P"), ("NP", "S", 0), ("CC", "0A", 0), ("NP", "P", 0)),

	(("DP", "P"), ("DP", "P", 0), ("CC", "0A", 0), ("DP", "S", 0)),
	(("DP", "P"), ("DP", "S", 0), ("CC", "0A", 0), ("DP", "S", 0)),
	(("DP", "P"), ("DP", "P", 0), ("CC", "0A", 0), ("DP", "P", 0)),
	(("DP", "P"), ("DP", "S", 0), ("CC", "0A", 0), ("DP", "P", 0)),

	(("NP", "P"), ("NP", "P", 0), ("CC", "0O", 0), ("NP", "S", 0)),
	(("NP", "P"), ("NP", "S", 0), ("CC", "0O", 0), ("NP", "S", 0)),
	(("NP", "P"), ("NP", "P", 0), ("CC", "0O", 0), ("NP", "P", 0)),
	(("NP", "P"), ("NP", "S", 0), ("CC", "0O", 0), ("NP", "P", 0)),

	(("DP", "S"), ("DP", "P", 0), ("CC", "0O", 0), ("DP", "S", 0)),
	(("DP", "S"), ("DP", "S", 0), ("CC", "0O", 0), ("DP", "S", 0)),
	(("DP", "P"), ("DP", "P", 0), ("CC", "0O", 0), ("DP", "P", 0)),
	(("DP", "P"), ("DP", "S", 0), ("CC", "0O", 0), ("DP", "P", 0)),

	(("I'", ""), ("I'", ""), ("CC", "0A", 0), ("I'", "")),
	(("I'", ""), ("I'", ""), ("CC", "0O", 0), ("I'", "")),

	# TODO: add IP for and/or
	#       and the remaining pos types for either/or and neither/nor

	(("IP", ""), ("CC", "0E", 0), ("IP", ""), ("CC", "0O", 0), ("IP", "")),

	(("DP", "S"), ("CC", "0I", 0), ("DP", "S"), ("CC", "0R", 0), ("DP", "S")),
	(("DP", "S"), ("CC", "0I", 0), ("DP", "P"), ("CC", "0R", 0), ("DP", "S")),
	(("DP", "P"), ("CC", "0I", 0), ("DP", "S"), ("CC", "0R", 0), ("DP", "P")),
	(("DP", "P"), ("CC", "0I", 0), ("DP", "P"), ("CC", "0R", 0), ("DP", "P")),
]

# vocab format is (word, part of speech, selection parameters, other parameters)
# part of speech: "NAME" = name/proper noun, "N" = noun, "P": preposition
# selection parameters: "0" = no complements, "n" = NP, "d" = DP
# selection parameters do not get passed up the chain
# and are only used to select complements
# other parameters get passed up chain
vocabulary = [
    # Names
	("Arthur", "NAME", "0", "S"),
	("Guinevere", "NAME", "0", "S"),
	("Sir Lancelot", "NAME", "0", "S"),
	("Sir Bedevere", "NAME", "0", "S"),
	("Zoot", "NAME", "0", "S"),
	("Patsy", "NAME", "0", "S"),
	("Uther Pendragon", "NAME", "0", "S"),

	# nouns
	("king", "N", "0", "S"),
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

    # plural nouns
    ("coconuts", "N", "0", "P"),
    ("halves", "N", "0", "P"),
    ("snows", "N", "0", "P"),
    ("mountains", "N", "0", "P"),
    ("areas", "N", "0", "P"),
    ("strangers", "N", "0", "P"),
    ("inches", "N", "0", "P"),
	("snakes", "N", "0", "P"),
    ("ants", "N", "0", "P"),
    ("nights", "N", "0", "P"),

    # proper nouns, not people -- need to do more
    ("Camelot", "NAME", "0", "S"),
    ("England", "NAME", "0", "S"),
    ("the Holy Grail", "NAME", "0", "S"),
    ("the Round Table", "NAME", "0", "S"),

    # plural proper nouns -- need to do more
    ("Britons", "N", "0", "P"),
    ("Saxons", "N", "0", "P"),

    # personal pronouns -- need to do more
	# TODO: separate subject / object
    ("he", "Pn", "0", "S"),
    #("her", "Pn", "0", "S"),
    #("him", "Pn", "0", "S"),
    ("it", "Pn", "0", "S"),
    ("one", "Pn", "0", "S"),
    ("she", "Pn", "0", "S"),
    #("them", "Pn", "0", "P"),
    ("they", "Pn", "0", "P"),

    # personal possessive pronouns
    ("her", "X", "n", "S"),
    ("his", "X", "n", "S"),
    ("its", "X", "n", "S"),
    ("their", "X", "n", "P"),

    # adverbs -- need to do more
    ("again", "Adv", "0", ""),
    ("already", "Adv", "0", ""),
    ("currently", "Adv", "0", ""),
    ("frequently", "Adv", "0", ""),
    ("precisely", "Adv", "0", ""),
    ("south", "Adv", "0", ""),
    ("successfully", "Adv", "0", ""),
    ("unfortunately", "Adv", "0", ""),

	("that", "C", "i"),
    
    # prepositions
	("of", "P", "d"),
	("above", "P", "d"),
	("across", "P", "d"),
	("at", "P", "d"),
	("below", "P", "d"),
	("by", "P", "d"),
	("for", "P", "d"),
	("from", "P", "d"),
	("into", "P", "d"),
	("near", "P", "d"),
	("on", "P", "d"),
	("over", "P", "d"),
	("through", "P", "d"),
    ("to", "P", "d"),
	("with", "P", "d"),
    
    # determiners
	("a", "D", "n", "S"),
	("another", "D", "n", "S"),
	("any", "D", "n", "S"),
	("any", "D", "n", "P"),
	("each", "D", "n", "S"),
	("every", "D", "n", "S"),
	("no", "D", "n", "P"),
	("that", "D", "n", "S"),
	("the", "D", "n", "S"),
	("the", "D", "n", "P"),
	("this", "D", "n", "S"),

	# wh words
	("what", "Q", "0"),
	("who", "Q", "0"),
	("where", "Q", "0"),
	#("why", "Q", "0"),

	# wh determiners
	("that", "X", ""),
	("what", "X", ""),
	("which", "X", ""),

	# wh pronouns
	("what", "X", ""),
	("who", "X", ""),

	# wh possessive pronouns
	("whose", "X", ""),

	# wh adverbs
	("how", "X", ""),
	("when", "X", ""),
	("where", "X", ""),
	("why", "X", ""),

	("cat", "N", "0"),
	("dog", "N", "0"),
	("bunny", "N", "0"),
	#("run", "V", "0"),
	#("eat", "V", "0d"),
	#("give", "V", "0"), # will handle indirect objects later
	#("does", "I", "v"),
	#("did", "I", "v"),
	#("will", "I", "v"),

    # end of sentence
	(".", ".", "0"),
	("!", ".", "0"),
	("?", "?", "0"),

	# pauses -- need to do more
	(",", "Pause_,", "0", ""),
	("...", "X", "", ""),
	("--", "X", "", ""),
	(";", "X", "", ""),
	(":", "X", "", ""),

	# possessive marker
	("'s", "X", ""),

	# coordinating conjunctions -- need to do more
	("and", "CC", "0", "A"),
	("but", "X", "", ""),
	("or", "CC", "0", "O"),
	("either", "CC", "0", "E"),
	("nor", "CC", "0", "R"),
	("neither", "CC", "0", "I"),
	("so", "X", "", ""),

	# subordinating conjunctions -- need to do more
	("that", "SC", "", ""),
	("so", "SC", "", ""),
	("while", "SC", "", ""),
	("because", "SC", "", ""),
	("if", "X", "SC", ""),

	# adjectives -- need to do more
	("bloody", "A", "_", ""),
	("weary", "A", "_", ""),
	("unable", "A", "_", ""),
	("trusty", "A", "_", ""),
	("further", "A", "_", ""),
	("sacred", "A", "_", ""),
	("tropical", "A", "_", ""),
	("indigenous", "A", "_", ""),
	("temperate", "A", "_", ""),
	("hot", "A", "_", ""),
	("lucky", "A", "_", ""),
	("simple", "A", "_", ""),
	("tiny", "A", "_", ""),
	("hard", "A", "_", ""),
	("sensational", "A", "_", ""),
	("comparable", "A", "_", ""),
	("angolian", "A", "_", ""),
	("yellow", "A", "_", ""),
	("plodding", "A", "_", ""),

	# comparative adjectives -- need to do more
	("bloodier", "X", "", ""),
	("wearier", "X", "", ""),
	("trustier", "X", "", ""),
	("hotter", "X", "", ""),
	("simpler", "X", "", ""),
	("tinier", "X", "", ""),
	("harder", "X", "", ""),

	# superlative adjectives -- need to do more
	("bloodiest", "X", "", ""),
	("weariest", "X", "", ""),
	("trustiest", "X", "", ""),
	("hottest", "X", "", ""),
	("simplest", "X", "", ""),
	("tiniest", "X", "", ""),
	("hardest", "X", "", ""),

	# numbers -- need to do more
	("eight", "Num", "", "P"),
	("five", "Num", "", "P"),
	("one", "Num", "", "S"),
	("5.5", "Num", "", "P"),
	("sixty", "Num", "", "P"),
	("5,000", "Num", "", "P"),

	# expletives -- need to do more
	("there", "X", "", ""),

	# 'to'
	("to", "X", "", ""),

	# 'not'
	("not", "X", "", ""),


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
	("had", "I", "_", "HS"),
	("had", "I", "_", "HP"),
	("has", "I", "_", "HS"),
	("have", "I", "_", "HP"),
	("have", "I", "_", "HB"),

	# modal inflectors
	("can", "I", "_", "M"),
	("may", "I", "_", "M"),
	("might", "I", "_", "M"),
	("must", "I", "_", "M"),
	("shall", "I", "_", "M"),
	("should", "I", "_", "M"),
	("would", "I", "_", "M"),
	("could", "I", "_", "M"),
	("will", "I", "_", "M"),
	("ought", "I", "_", "M"),

	# VERBS
	# R: root
	# S: singular
	# P: plural
	# T: past
	# G: progressive
	# N: perfect nonprogressive
	#
	# Selection parameters
	#   0: can be intransitive
	#   d: can be transitive and selects for DP
	#   c: can be transitive and selects for CP
	#   p: can be transitive and selects for PP
	#   a: can be transitive and selects for AP
	("knew", "V", "0dc", "PT"),
	("knew", "V", "0dc", "ST"),
	("know", "V", "0dc", "P"),
	("know", "V", "0dc", "R"),
	("knowing", "V", "0dc", "G"),
	("known", "V", "0dc", "N"),    # TODO: deal with passive voice later
	("knows", "V", "0dc", "S"),

	("is", "V", "dpa", "S"),
	("was", "V", "dpa", "ST"),
	("are", "V", "dpa", "P"),
	("were", "V", "dpa", "PT"),
	("be", "V", "dpa", "R"),
	("being", "V", "dpa", "G"),
	("been", "V", "dpa", "N"),

	("has", "V", "d", "S"),
	("had", "V", "d", "PT"),
	("had", "V", "d", "ST"),
	("had", "V", "d", "N"),
	("have", "V", "d", "R"),
	("have", "V", "d", "P"),
	("having", "V", "d", "G"),

	("cover", "V", "dp", "R"),
	("cover", "V", "dp", "P"),
	("covers", "V", "dp", "S"),
	("covered", "V", "dp", "ST"),
	("covered", "V", "dp", "PT"),
	("covered", "V", "dp", "N"),
	("covering", "V", "dp", "G"),

	("drink", "V", "0dp", "R"),
	("drink", "V", "0dp", "P"),
	("drinks", "V", "0dp", "S"),
	("drank", "V", "0dp", "ST"),
	("drank", "V", "0dp", "PT"),
	("drinking", "V", "0dp", "G"),
	("drunk", "V", "0dp", "N"),

	("carry", "V", "dp", "R"),
	("carry", "V", "dp", "P"),
	("carries", "V", "dp", "S"),
	("carried", "V", "dp", "ST"),
	("carried", "V", "dp", "PT"),
	("carried", "V", "dp", "N"),
	("carrying", "V", "dp", "G"),

	("ride", "V", "0dp", "R"),
	("ride", "V", "0dp", "P"),
	("rides", "V", "0dp", "S"),
	("rode", "V", "0dp", "ST"),
	("rode", "V", "0dp", "PT"),
	("riding", "V", "0dp", "G"),
	("ridden", "V", "0dp", "N"),

	("speak", "V", "0p", "R"),
	("speak", "V", "0p", "P"),
	("speaks", "V", "0p", "S"),
	("spoke", "V", "0p", "ST"),
	("spoke", "V", "0p", "PT"),
	("speaking", "V", "0p", "G"),
	("spoken", "V", "0p", "N"),

	("grow", "V", "0", "R"),
	("grow", "V", "0", "P"),
	("grows", "V", "0", "S"),
	("grew", "V", "0", "ST"),
	("grew", "V", "0", "PT"),
	("growing", "V", "0", "G"),
	("grown", "V", "0", "N"),

	("suggest", "V", "c", "R"),
	("suggest", "V", "c", "P"),
	("suggests", "V", "c", "S"),
	("suggested", "V", "c", "ST"),
	("suggested", "V", "c", "PT"),
	("suggested", "V", "c", "N"),
	("suggesting", "V", "c", "G"),

	("migrate", "V", "0p", "R"),
	("migrate", "V", "0p", "P"),
	("migrates", "V", "0p", "S"),
	("migrated", "V", "0p", "ST"),
	("migrated", "V", "0p", "PT"),
	("migrated", "V", "0p", "N"),
	("migrating", "V", "0p", "G"),

	("do", "V", "0d", "R"),
	("do", "V", "0d", "P"),
	("does", "V", "0d", "S"),

	("goes", "V", "0p", "S"),
]

# types of complements each head can have
selection_rules = {
	"V": "0dcpa",
	"I": "_",
	"N": "0",
	"D": "n",
	"P": "d",
	"NAME": "0",
	".": "0",
	"?": "0",
	"CC": "0",
}

vocab_parameters = collections.defaultdict(str, {
	"V": "RSPGNT",
	"I": "DPSV*%$HTM",
	"N": "SP",
	"D": "SP",
	"CC": "A",
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
        if not (len(r) > 2 and r[2] == 0)
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

	# filter out terms that can't terminate
	terminatable = {
		v[0]
		for v in vocabulary
	}
	while True:
		initial_length = len(terminatable)

		terminatable |= {
			rule[0]
			for rule in grammar
			if all([
				r in terminatable
				for r in rule[1]
			])
		}

		# if didn't add anything we're done
		if len(terminatable) == initial_length:
			break
	# remove rules
	grammar = [
		rule
		for rule in grammar
		if all([
			r in terminatable
			for r in rule[1]
		])
	]

	# filter out unusued rules that can't derive anything
	#while False:
	#while True:
	#	initial_length = len(grammar)
	#	# terms are invalid if cannot derive anything
	#	valid = {
	#		rule[0]
	#		for rule in grammar
	#	} | {
	#		word[0]
	#		for word in vocabulary
	#	}
	#	grammar = [
	#		rule
	#		for rule in grammar
	#		if all(
	#			tag in valid
	#			for tag in rule[1]
	#		)
	#	]

	#	# if didn't remove anything we're done
	#	if len(grammar) == initial_length:
	#		break

	return grammar

def is_recursive(rule):
	return rule[0] in rule[1]

def to_string(grammar):
	return "\n".join(
		"\t".join((
			".1" if is_recursive(rule) else "1",
			rule[0],
			" ".join(rule[1]),
		)) for rule in grammar
	)

print(to_string(gen_grammar(rules)))

#pdb.set_trace()

