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
	(1, ("IP", ""), ("DP", "SJ", 0), ("I'", "S")),  # singular
	(1, ("IP", ""), ("DP", "PJ", 0), ("I'", "P")),  # plural

	# imperative
	(1e-3, ("S", ""), ("I'", "P"), (".", "")),

	(1, ("S", ""), ("CP", "."), (".", "")),
	#(("S", ""), ("CP", "?"), ("?", "")),

	(1, ("CP", "."), ("IP", "")), # null complementizer (forced)

	(1, ("CP", ""), ("IP", "")), # null complementizer
	(1, ("CP", ""), ("C", "i"), ("IP", "")),

	#(("CP", "?"), ("I", "v"), ("IP", "m")), # I to C movement
	#(("IP", "m"), ("DP", ""), ("I'", "m")),
	#(("I'", "m"), ("VP", "")), # move/missing inflector

	# null determiner
	(1, ("DP", ""), ("NAME", "0")),
    (1, ("DP", ""), ("Pn", "0")),
	(1, ("DP", "P"), ("NP", "P")),

	# PP adjuncts
	(.1, ("VP", ""), ("VP", ""), ("PP", "", 0)),
	(.1, ("NP", ""), ("NP", ""), ("PP", "", 0)),
	(.1, ("VP", "W"), ("VP", ""), ("PP", "W", 0)),
	(.1, ("NP", "W"), ("NP", ""), ("PP", "W", 0)),

	# CP adjunct
	(.1, ("NP", ""), ("NP", ""), ("CP", "a")),
	(.1, ("CP", "a"), ("C", "i"), ("IP", "a")),
	(.1, ("IP", "a"), ("I'", "")), # IP with no subject

	# head complements
	# no complements
	(1, ("NP", ""), ("N", "0")),
    (1, ("NsaP", ""), ("Nsa", "0")),
	(1, ("VP", ""), ("V", "0")),
	(1, (".", ""), (".", "0")),
	(1, ("?", ""), ("?", "0")),
	# VP complements
	#(("I'", ""), ("I", "v"), ("VP", "")),
	# DP complements
	(1, ("VP", ""), ("V", "d"), ("DP", "SO", 0)),
	(1, ("VP", ""), ("V", "d"), ("DP", "PO", 0)),
	(1, ("PP", ""), ("P", "d"), ("DP", "PO")),
	(1, ("PP", ""), ("P", "d"), ("DP", "SO")),
	(1, ("VP", "W"), ("V", "d")),
	(1, ("PP", "W"), ("P", "d")),
	# NP complements
	(1, ("DP", "SO"), ("D", "Sn"), ("NP", "SO")),
	(1, ("DP", "SJ"), ("D", "Sn"), ("NP", "SJ")),
	(1, ("DP", "PO"), ("D", "nP"), ("NP", "PO")),
	(1, ("DP", "PJ"), ("D", "nP"), ("NP", "PJ")),
	# CP complements
	(1, ("VP", ""), ("V", "c"), ("CP", "", 0)),
	(1, ("VP", "I"), ("V", "Ic"), ("CP", "", 0)),
	(1, ("VP", "W"), ("V", "c"), ("CP", "W", 0)),
    # AP complements
    (1, ("VP", ""), ("V", "a"), ("AP", "", 0)),
    # PP complements
    (1, ("VP", ""), ("V", "p"), ("PP", "", 0)),
	(1, ("VP", "I"), ("V", "Ip"), ("PP", "", 0)),
	# root form CP complements
	(1, ("VP", ""), ("V", "r"), ("CP", "F", 0)),
	(1, ("VP", "W"), ("V", "r"), ("CP", "FW", 0)),

	# inflection rules
	# I' parameters:
	# V: voice
	# T: progressive aspect
	# A: perfect aspect
	# M: modality
	(1, ("VP", "P"), ("VP", "")),

	(1, ("I'", "R"), ("VP", "R")), # root
	(1, ("I'", "G"), ("VP", "G")), # progressive
	(1, ("I'", "N"), ("VP", "N")), # perfect nonprogressive

	(1e-3, ("I'", "G"), ("I", "$_", 0), ("VP", "I")), # passive progressive, eg being known
	(1e-3, ("I'", "N"), ("I", "%_", 0), ("VP", "N")), # perfect nonprogressive, eg been known
	(1, ("I'", "N"), ("I", "%_", 0), ("VP", "G")), # perfect nonprogressive, eg been knowing
	(1e-3, ("I'", "R"), ("I", "*_", 0), ("VP", "I")), # eg be known
	(1, ("I'", "R"), ("I", "*_", 0), ("VP", "G")), # eg be knowing

	(1, ("I'", "P"), ("VP", "P")), # active plural, eg know
	(1, ("I'", "S"), ("VP", "S")), # active singular, eg knows
	(1, ("I'", "P"), ("VP", "PT")), # past plural, eg knew
	(1, ("I'", "S"), ("VP", "ST")), # past singular, eg knew
	(1, ("I'", "P"), ("I", "DP_", 0), ("VP", "R")), # active plural, eg do know
	(1, ("I'", "S"), ("I", "DS_", 0), ("VP", "R")), # active singular, eg does know;
	(1e-3, ("I'", "P"), ("I", "VP_", 0), ("VP", "I")), # passive plural, eg are known
	(1e-3, ("I'", "S"), ("I", "VS_", 0), ("VP", "I")), # passive singular, eg is known

	(1, ("VP", "I"), ("V", "0I")),

	(1, ("I'", "S"), ("I", "VS_", 0), ("I'", "G")), # continuous singular, eg is knowing
	(1, ("I'", "P"), ("I", "VP_", 0), ("I'", "G")), # continuous plural, eg are knowing

	(1, ("I'", "R"), ("I", "HB_", 0), ("I'", "N")), # have known

	(1, ("I'", "S"), ("I", "M_", 0), ("I'", "R")), # modality, eg should know
	(1, ("I'", "P"), ("I", "M_", 0), ("I'", "R")), # modality, eg should know

	# I to C movement
	# TODO: prohibit null inflector movement (i don't know where it's coming from...)
	(1, ("VP", "C"), ("DP", "SJ", 0), ("VP", "")), # the horse know
	(1, ("VP", "C"), ("DP", "PJ", 0), ("VP", "")), # the snakes know
	(1, ("I'", "C"), ("DP", "SJ", 0), ("I'", "")), # the horse knowing
	(1, ("I'", "C"), ("DP", "PJ", 0), ("I'", "")), # the snakes knowing
	(1, ("IP", "C"), ("I'", "CS")), # does the horse know
	(1, ("IP", "C"), ("I'", "CP")), # do the snakes know
	(1e-3, ("S", ""), ("IP", "C"), ("?", "")), # does the horse know ?

	# how/why
	(1, ("HP", ""), ("H", ""), ("IP", "C")), # how does the horse know
	(1e-3, ("S", ""), ("HP", ""), ("?", "")), # how does the horse know ?

	# CP with root form VP
	(1, ("CP", "F"), ("DP", "SJ", 0), ("VP", "R")), # she carry
	(1, ("CP", "F"), ("DP", "SJ", 0), ("I", "*_", 0), ("VP", "I", 0)), # she be carried (passive sing.)
	(1, ("CP", "F"), ("DP", "PJ", 0), ("I", "*_", 0), ("VP", "I")), # she be carried (passive plural)
	(1, ("CP", "F"), ("C", "i", 0), ("DP", "SJ", 0), ("VP", "R")), # that she carry
	(1, ("CP", "F"), ("C", "i", 0), ("DP", "SJ", 0), ("I", "*_", 0), ("VP", "I", 0)), # that she be carried (passive sing.)
	(1, ("CP", "F"), ("C", "i", 0), ("DP", "PJ", 0), ("I", "*_", 0), ("VP", "I")), # that she be carried (passive plural)

	# wh movement
	(1, ("WP", ""), ("W", ""), ("IP", "CW")), # what does the horse know
	(1e-3, ("S", ""), ("WP", ""), ("?", "")), # what does the horse know ?
	(1e-3, ("DP", "SO"), ("W", ""), ("IP", "W")), # what the horse knows
	(1e-3, ("DP", "SJ"), ("W", ""), ("IP", "W")), # what the horse knows

	# negation
	# TODO: prohibit consecutive "not"s
	(1e-3, ("VP", ""), ("Neg", "", 0), ("VP", "")), # not know
	(1e-3, ("I'", ""), ("Neg", "", 0), ("I'", "")), # not know

	# verb as subject
	(1e-3, ("DP", "SO"), ("VP", "G")),
	(1e-3, ("DP", "SJ"), ("VP", "G")),

	# adjectives
	(1, ("AP", ""), ("A", "_")),
	(1, ("DP", "O"), ("D", "n"), ("AP", "", 0), ("NP", "O")),
	(1, ("DP", "J"), ("D", "n"), ("AP", "", 0), ("NP", "J")),
    (1, ("DP", "O"), ("D", "n"), ("NsaP", "O")),
    (1, ("DP", "J"), ("D", "n"), ("NsaP", "J")),

	# adverbs
	(1, ("AdvP", ""), ("Adv", "0")),
    (.1, ("VP", ""), ("VP", ""), ("AdvP", "", 0)),
    (.1, ("VP", ""), ("AdvP", "", 0), ("VP", "")),

    # numbers
    (1, ("DP", "PO"), ("D", "Pn"), ("Num", "P"), ("AP", "", 0), ("NP", "PO")),
    (1, ("DP", "SO"), ("D", "Sn"), ("Num", "S"), ("AP", "", 0), ("NP", "SO")),
    (1, ("DP", "PJ"), ("D", "nP"), ("Num", "P"), ("AP", "", 0), ("NP", "PJ")),
    (1, ("DP", "SJ"), ("D", "nS"), ("Num", "S"), ("AP", "", 0), ("NP", "SJ")),
    (1, ("DP", "PO"), ("D", "nP"), ("Num", "P"), ("NP", "PO")),
    (1, ("DP", "SO"), ("D", "nS"), ("Num", "S"), ("NP", "SO")),
    (1, ("DP", "PJ"), ("D", "nP"), ("Num", "P"), ("NP", "PJ")),
    (1, ("DP", "SJ"), ("D", "nS"), ("Num", "S"), ("NP", "SJ")),
    (1, ("DP", "PO"), ("Num", "P"), ("NP", "PO")),
    (1, ("DP", "SO"), ("Num", "S"), ("NP", "SO")),
    (1, ("DP", "PJ"), ("Num", "P"), ("NP", "PJ")),
    (1, ("DP", "SJ"), ("Num", "S"), ("NP", "SJ")),
    (1, ("DP", "PO"), ("Num", "P"), ("AP", "", 0), ("NP", "PO")),
    (1, ("DP", "SO"), ("Num", "S"), ("AP", "", 0), ("NP", "SO")),
    (1, ("DP", "PJ"), ("Num", "P"), ("AP", "", 0), ("NP", "PJ")),
    (1, ("DP", "SJ"), ("Num", "S"), ("AP", "", 0), ("NP", "SJ")),

    # personal possessive pronouns
    (1, ("Poss", ""), ("PerPro", "0")),
    (1e-3, ("Poss", ""), ("DP", "S", 0), ("PosMar", "0", 0)),
    (1, ("DP", "O"), ("Poss", ""), ("NP", "O")),
    (1, ("DP", "J"), ("Poss", ""), ("NP", "J")),

    # pause
    (1e-3, ("DP", ""), ("DP", ""), ("Pause_,", "0", 0), ("DP", "SO", 0)),
    (1e-3, ("DP", ""), ("DP", ""), ("Pause_,", "0", 0), ("DP", "PO", 0)),
    (1e-3, ("DP", ""), ("DP", ""), ("Pause_,", "0", 0), ("DP", "SO", 0), ("Pause_,", "0", 0)),
    (1e-3, ("DP", ""), ("DP", ""), ("Pause_,", "0", 0), ("DP", "PO", 0), ("Pause_,", "0", 0)),
    (1e-3, ("IP", ""), ("SP", "v"), ("Pause_,", "0", 0), ("IP", "")),
	(1e-3, ("IP", ""), ("IP", ""), ("Pause_,", "0", 0), ("SentC", "", 0), ("IP", "")),
    (1e-3, ("IP", ""), ("IP", ""), ("Pause_;", "0", 0), ("IP", "")), 
    (1e-3, ("DP", ""), ("DP", ""), ("Pause_:", "0", 0), ("DP", "")),

	# coordinating conjunctions
	(.1, ("NP", "P"), ("NP", "P", 0), ("CC", "0A", 0), ("NP", "S", 0)),
	(.1, ("NP", "P"), ("NP", "S", 0), ("CC", "0A", 0), ("NP", "S", 0)),
	(.1, ("NP", "P"), ("NP", "P", 0), ("CC", "0A", 0), ("NP", "P", 0)),
	(.1, ("NP", "P"), ("NP", "S", 0), ("CC", "0A", 0), ("NP", "P", 0)),

	(.1, ("DP", "PO"), ("DP", "PO", 0), ("CC", "0A", 0), ("DP", "SO", 0)),
	(.1, ("DP", "PJ"), ("DP", "PJ", 0), ("CC", "0A", 0), ("DP", "SJ", 0)),
	(.1, ("DP", "PO"), ("DP", "SO", 0), ("CC", "0A", 0), ("DP", "SO", 0)),
	(.1, ("DP", "PJ"), ("DP", "SJ", 0), ("CC", "0A", 0), ("DP", "SJ", 0)),
	(.1, ("DP", "PO"), ("DP", "PO", 0), ("CC", "0A", 0), ("DP", "PO", 0)),
	(.1, ("DP", "PJ"), ("DP", "PJ", 0), ("CC", "0A", 0), ("DP", "PJ", 0)),
	(.1, ("DP", "PO"), ("DP", "SO", 0), ("CC", "0A", 0), ("DP", "PO", 0)),
	(.1, ("DP", "PJ"), ("DP", "SJ", 0), ("CC", "0A", 0), ("DP", "PJ", 0)),

	(.1, ("NP", "P"), ("NP", "P", 0), ("CC", "0O", 0), ("NP", "S", 0)),
	(.1, ("NP", "P"), ("NP", "S", 0), ("CC", "0O", 0), ("NP", "S", 0)),
	(.1, ("NP", "P"), ("NP", "P", 0), ("CC", "0O", 0), ("NP", "P", 0)),
	(.1, ("NP", "P"), ("NP", "S", 0), ("CC", "0O", 0), ("NP", "P", 0)),

	(.1, ("DP", "SO"), ("DP", "PO", 0), ("CC", "0O", 0), ("DP", "SO", 0)),
	(.1, ("DP", "SJ"), ("DP", "PJ", 0), ("CC", "0O", 0), ("DP", "SJ", 0)),
	(.1, ("DP", "SO"), ("DP", "SO", 0), ("CC", "0O", 0), ("DP", "SO", 0)),
	(.1, ("DP", "SJ"), ("DP", "SJ", 0), ("CC", "0O", 0), ("DP", "SJ", 0)),
	(.1, ("DP", "PO"), ("DP", "PO", 0), ("CC", "0O", 0), ("DP", "PO", 0)),
	(.1, ("DP", "PJ"), ("DP", "PJ", 0), ("CC", "0O", 0), ("DP", "PJ", 0)),
	(.1, ("DP", "PO"), ("DP", "SO", 0), ("CC", "0O", 0), ("DP", "PO", 0)),
	(.1, ("DP", "PJ"), ("DP", "SJ", 0), ("CC", "0O", 0), ("DP", "PJ", 0)),

	(.1, ("I'", ""), ("I'", ""), ("CC", "0A", 0), ("I'", "")),
	(.1, ("I'", ""), ("I'", ""), ("CC", "0O", 0), ("I'", "")),

	# TODO: add IP for and/or
	#       and the remaining pos types for either/or and neither/nor

	(.1, ("IP", ""), ("CC", "0E", 0), ("IP", ""), ("CC", "0O", 0), ("IP", "")),

	(.1, ("DP", "S"), ("CC", "0I", 0), ("DP", "S"), ("CC", "0R", 0), ("DP", "S")),
	(.1, ("DP", "S"), ("CC", "0I", 0), ("DP", "P"), ("CC", "0R", 0), ("DP", "S")),
	(.1, ("DP", "P"), ("CC", "0I", 0), ("DP", "S"), ("CC", "0R", 0), ("DP", "P")),
	(.1, ("DP", "P"), ("CC", "0I", 0), ("DP", "P"), ("CC", "0R", 0), ("DP", "P")),

	# subordinate phrases
	(1e-3, ("VP", ""), ("VP", ""), ("SP", "v", 0)),
	(1e-3, ("DP", ""), ("DP", ""), ("SP", "n", 0)),
	(1e-3, ("DP", "J"), ("DP", "J"), ("SC", "d", 0), ("I'", "")),
	(1e-3, ("DP", "O"), ("DP", "O"), ("SC", "d", 0), ("I'", "")),
	(1, ("SP", "v"), ("SC", "v"), ("IP", "", 0)),
	(1, ("SP", "n"), ("SC", "n"), ("IP", "", 0)),

	# wh subjects
	(1e-5, ("WP", ""), ("W", ""), ("I'", "S")),
	(1e-5, ("WP", ""), ("W", ""), ("I'", "P")),
	(1e-5, ("WP", ""), ("WHDET", "", 0), ("NP", "SO"), ("I'", "S")),
	(1e-5, ("WP", ""), ("WHDET", "", 0), ("NP", "SJ"), ("I'", "S")),
	(1e-5, ("WP", ""), ("WHDET", "", 0), ("NP", "PO"), ("I'", "P")),
	(1e-5, ("WP", ""), ("WHDET", "", 0), ("NP", "PJ"), ("I'", "P")),
]

# vocab format is (word, part of speech, selection parameters, other parameters)
# part of speech: "NAME" = name/proper noun, "N" = noun, "P": preposition
# selection parameters: "0" = no complements, "n" = NP, "d" = DP
# selection parameters do not get passed up the chain
# and are only used to select complements
# other parameters get passed up chain
vocabulary = [
    # Names - split proper nouns
	("Arthur", "NAME", "0", "SO"),
    ("Arthur", "NAME", "0", "SJ"),
    ("Sir Arthur", "NAME", "0", "SO"),
    ("Sir Arthur", "NAME", "0", "SJ"),
    ("Sir Arthur Pendragon", "NAME", "0", "SO"),
    ("Sir Arthur Pendragon", "NAME", "0", "SJ"),
    ("Arthur Pendragon", "NAME", "0", "SO"),
    ("Arthur Pendragon", "NAME", "0", "SJ"),
	("Guinevere", "NAME", "0", "SO"),
	("Guinevere", "NAME", "0", "SJ"),
    ("Sir Guinevere", "NAME", "0", "SO"),
    ("Sir Guinevere", "NAME", "0", "SJ"),
    ("Sir Guinevere Pendragon", "NAME", "0", "SO"),
    ("Sir Guinevere Pendragon", "NAME", "0", "SJ"),
    ("Guinevere Pendragon", "NAME", "0", "SO"),
    ("Guinevere Pendragon", "NAME", "0", "SJ"),
    ("Lancelot", "NAME", "0", "SO"),
    ("Lancelot", "NAME", "0", "SJ"),
	("Sir Lancelot", "NAME", "0", "SO"),
	("Sir Lancelot", "NAME", "0", "SJ"),
    ("Lancelot Pendragon", "NAME", "0", "SO"),
    ("Lancelot Pendragon", "NAME", "0", "SJ"),
    ("Sir Lancelot Pendragon", "NAME", "0", "SO"),
    ("Sir Lancelot Pendragon", "NAME", "0", "SJ"),
    ("Bedevere", "NAME", "0", "SO"),
    ("Bedevere", "NAME", "0", "SJ"),
	("Sir Bedevere", "NAME", "0", "SO"),
	("Sir Bedevere", "NAME", "0", "SJ"),
    ("Sir Bedevere Pendragon", "NAME", "0", "SO"),
    ("Sir Bedevere Pendragon", "NAME", "0", "SJ"),
    ("Bedevere Pendragon", "NAME", "0", "SO"),
    ("Bedevere Pendragon", "NAME", "0", "SJ"),
	("Zoot", "NAME", "0", "SO"),
	("Zoot", "NAME", "0", "SJ"),
    ("Sir Zoot", "NAME", "0", "SO"),
    ("Sir Zoot", "NAME", "0", "SJ"),
    ("Sir Zoot Pendragon", "NAME", "0", "SO"),
    ("Sir Zoot Pendragon", "NAME", "0", "SJ"),
    ("Zoot Pendragon", "NAME", "0", "SO"),
    ("Zoot Pendragon", "NAME", "0", "SJ"),
	("Patsy", "NAME", "0", "SO"),
	("Patsy", "NAME", "0", "SJ"),
    ("Sir Patsy", "NAME", "0", "SO"),
    ("Sir Patsy", "NAME", "0", "SJ"),
    ("Sir Patsy Pendragon", "NAME", "0", "SO"),
    ("Sir Patsy Pendragon", "NAME", "0", "SJ"),
    ("Patsy Pendragon", "NAME", "0", "SO"),
    ("Patsy Pendragon", "NAME", "0", "SJ"),
    ("Uther", "NAME", "0", "SO"),
    ("Uther", "NAME", "0", "SJ"),
    ("Sir Uther", "NAME", "0", "SO"),
    ("Sir Uther", "NAME", "0", "SJ"),
    ("Sir Uther Pendragon", "NAME", "0", "SO"),
    ("Sir Uther Pendragon", "NAME", "0", "SJ"),
	("Uther Pendragon", "NAME", "0", "SO"),
	("Uther Pendragon", "NAME", "0", "SJ"),
    ("Dingo", "NAME", "0", "SO"),
    ("Dingo", "NAME", "0", "SJ"),
    ("Sir Dingo", "NAME", "0", "SO"),
    ("Sir Dingo", "NAME", "0", "SJ"),
    ("Sir Dingo Pendragon", "NAME", "0", "SO"),
    ("Sir Dingo Pendragon", "NAME", "0", "SJ"),
    ("Dingo Pendragon", "NAME", "0", "SO"),
    ("Dingo Pendragon", "NAME", "0", "SJ"),

	# nouns
	("castle", "N", "0", "SO"),
	("castle", "N", "0", "SJ"),
	("king", "N", "0", "SO"),
	("king", "N", "0", "SJ"),
	("defeater", "N", "0", "SO"),
	("defeater", "N", "0", "SJ"),
	("sovereign", "N", "0", "SO"),
	("sovereign", "N", "0", "SJ"),
	("servant", "N", "0", "SO"),
	("servant", "N", "0", "SJ"),
	("corner", "N", "0", "SO"),
	("corner", "N", "0", "SJ"),
	("land", "N", "0", "SO"),
	("land", "N", "0", "SJ"),
	("quest", "N", "0", "SO"),
	("quest", "N", "0", "SJ"),
	("chalice", "N", "0", "SO"),
	("chalice", "N", "0", "SJ"),
	("master", "N", "0", "SO"),
	("master", "N", "0", "SJ"),
	("horse", "N", "0", "SO"),
	("horse", "N", "0", "SJ"),
	("fruit", "N", "0", "SO"),
	("fruit", "N", "0", "SJ"),
	("swallow", "N", "0", "SO"),
	("swallow", "N", "0", "SJ"),
	("sun", "N", "0", "SO"),
	("sun", "N", "0", "SJ"),
	("winter", "N", "0", "SO"),
	("winter", "N", "0", "SJ"),
	("coconut", "N", "0", "SO"),
	("coconut", "N", "0", "SJ"),
	("pound", "N", "0", "SO"),
	("pound", "N", "0", "SJ"),
	("husk", "N", "0", "SO"),
	("husk", "N", "0", "SJ"),
	("home", "N", "0", "SO"),
	("home", "N", "0", "SJ"),
	("weight", "N", "0", "SO"),
	("weight", "N", "0", "SJ"),
	("story", "N", "0", "SO"),
	("story", "N", "0", "SJ"),

    # plural nouns
    ("coconuts", "N", "0", "PO"),
    ("coconuts", "N", "0", "PJ"),
    ("halves", "N", "0", "PO"),
    ("halves", "N", "0", "PJ"),
    ("snows", "N", "0", "PO"),
    ("snows", "N", "0", "PJ"),
    ("mountains", "N", "0", "PO"),
    ("mountains", "N", "0", "PJ"),
    ("areas", "N", "0", "PO"),
    ("areas", "N", "0", "PJ"),
    ("strangers", "N", "0", "PO"),
    ("strangers", "N", "0", "PJ"),
    ("inches", "N", "0", "PO"),
    ("inches", "N", "0", "PJ"),
	("snakes", "N", "0", "PO"),
	("snakes", "N", "0", "PJ"),
    ("ants", "N", "0", "PO"),
    ("ants", "N", "0", "PJ"),
    ("nights", "N", "0", "PO"),
    ("nights", "N", "0", "PJ"),

    # proper nouns, not people -- need to do more
    ("Camelot", "NAME", "0", "SO"),
    ("Camelot", "NAME", "0", "SJ"),
    ("England", "NAME", "0", "SO"),
    ("England", "NAME", "0", "SJ"),
    ("the Holy Grail", "NAME", "0", "SO"),
    ("the Holy Grail", "NAME", "0", "SJ"),
    ("the Round Table", "NAME", "0", "SO"),
    ("the Round Table", "NAME", "0", "SJ"),

    # plural proper nouns -- need to do more
    ("Britons", "N", "0", "PO"),
    ("Britons", "N", "0", "PJ"),
    ("Saxons", "N", "0", "PO"),
    ("Saxons", "N", "0", "PJ"),

    # personal pronouns -- need to do more
	# TODO: separate subject / object
    ("he", "Pn", "0", "SJ"),
    ("her", "Pn", "0", "SO"),
    ("him", "Pn", "0", "SO"),
    ("it", "Pn", "0", "SO"),
    ("it", "Pn", "0", "SJ"),
    ("one", "Pn", "0", "SO"),
    ("one", "Pn", "0", "SJ"),
    ("she", "Pn", "0", "SJ"),
    ("them", "Pn", "0", "PO"),
    ("they", "Pn", "0", "PJ"),

	("his", "Pn", "0", "S"),
	("his", "Pn", "0", "P"),
	("his", "PerPro", "0", "S"),
	("his", "PerPro", "0", "P"),

    # personal possessive pronouns
    ("her", "PerPro", "0", "S"),
    ("his", "PerPro", "0", "S"),
    ("its", "PerPro", "0", "S"),
    ("their", "PerPro", "0", "P"),

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
	("what", "W", ""),
	("who", "W", ""),
	("whose", "W", ""),
	("where", "W", ""),

	# wh-determiners
	("what", "WHDET", ""),
	("which", "WHDET", ""),
	("whose", "WHDET", ""),

	# wh adverbs
	("how", "H", ""),
	("why", "H", ""),
	("when", "H", ""),
	("where", "H", ""),

    # end of sentence
	(".", ".", "0"),
	("!", ".", "0"),
	("?", "?", "0"),

	# pauses -- need to do more
	(",", "Pause_,", "0", ""),
	("...", "Pause_...", "0", ""),
	("--", "Pause_--", "0", ""),
	(";", "Pause_;", "0", ""),
	(":", "Pause_:", "0", ""),

	# possessive marker
	("'s", "PosMar", "0", ""),

	# coordinating conjunctions -- need to do more
	("and", "CC", "0", "A"),
	("but", "X", "", ""),
	("or", "CC", "0", "O"),
	("either", "CC", "0", "E"),
	("nor", "CC", "0", "R"),
	("neither", "CC", "0", "I"),
	("so", "X", "", ""),

	# sentence conjunctions
	("and", "SentC", "", ""),
	("but", "SentC", "", ""),
	("or", "SentC", "", ""),
	("so", "SentC", "", ""),

	# subordinating conjunctions
	#  n - adjective clause with subject
	#  d - adjective clause without subject
	#  a - adverb clause
	("that", "SC", "nd", ""),
	("so", "SC", "v", ""),
	("while", "SC", "v", ""),
	("because", "SC", "v", ""),
	("if", "SC", "v", ""),
	("who", "SC", "d", ""),
	("when", "SC", "v", ""),
	("where", "SC", "n", ""),
	("why", "X", "v", ""),

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
	("Round", "A", "_", ""),
	("Holy", "A", "_", ""),

	# comparative adjectives -- need to do more
	("bloodier", "A", "_", ""),
	("wearier", "A", "_", ""),
	("trustier", "A", "_", ""),
	("hotter", "A", "_", ""),
	("simpler", "A", "_", ""),
	("tinier", "A", "_", ""),
	("harder", "A", "_", ""),

	# superlative adjectives -- need to do more
	("bloodiest", "A", "_", ""),
	("weariest", "A", "_", ""),
	("trustiest", "A", "_", ""),
	("hottest", "A", "_", ""),
	("simplest", "A", "_", ""),
	("tiniest", "A", "_", ""),
	("hardest", "A", "_", ""),
	
	("bloodiest", "Nsa", "0", "SO"),
	("weariest", "Nsa", "0", "SO"),
	("trustiest", "Nsa", "0", "SO"),
	("hottest", "Nsa", "0", "SO"),
	("simplest", "Nsa", "0", "SO"),
	("tiniest", "Nsa", "0", "SO"),
	("hardest", "Nsa", "0", "SO"),

	("bloodiest", "Nsa", "0", "SJ"),
	("weariest", "Nsa", "0", "SJ"),
	("trustiest", "Nsa", "0", "SJ"),
	("hottest", "Nsa", "0", "SJ"),
	("simplest", "Nsa", "0", "SJ"),
	("tiniest", "Nsa", "0", "SJ"),
	("hardest", "Nsa", "0", "SJ"),

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
	("not", "Neg", "", ""),


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
	("ought not to", "I", "_", "M"),
	("ought to", "I", "_", "M"),

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
	("known", "V", "0c", "I"),
	("known", "V", "0dc", "N"),
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
	("had", "V", "0", "I"),
	("had", "V", "d", "N"),
	("have", "V", "d", "R"),
	("have", "V", "d", "P"),
	("having", "V", "d", "G"),

	("cover", "V", "dp", "R"),
	("cover", "V", "dp", "P"),
	("covers", "V", "dp", "S"),
	("covered", "V", "dp", "ST"),
	("covered", "V", "dp", "PT"),
	("covered", "V", "0p", "I"),
	("covered", "V", "dp", "N"),
	("covering", "V", "dp", "G"),

	("drink", "V", "0dp", "R"),
	("drink", "V", "0dp", "P"),
	("drinks", "V", "0dp", "S"),
	("drank", "V", "0dp", "ST"),
	("drank", "V", "0dp", "PT"),
	("drinking", "V", "0dp", "G"),
	("drunk", "V", "0p", "I"),
	("drunk", "V", "0dp", "N"),

	("carry", "V", "dp", "R"),
	("carry", "V", "dp", "P"),
	("carries", "V", "dp", "S"),
	("carried", "V", "dp", "ST"),
	("carried", "V", "dp", "PT"),
	("carried", "V", "0p", "I"),
	("carried", "V", "dp", "N"),
	("carrying", "V", "dp", "G"),

	("ride", "V", "0dp", "R"),
	("ride", "V", "0dp", "P"),
	("rides", "V", "0dp", "S"),
	("rode", "V", "0dp", "ST"),
	("rode", "V", "0dp", "PT"),
	("riding", "V", "0dp", "G"),
	("ridden", "V", "0p", "I"),
	("ridden", "V", "0dp", "N"),

	("speak", "V", "0dp", "R"),
	("speak", "V", "0dp", "P"),
	("speaks", "V", "0dp", "S"),
	("spoke", "V", "0dp", "ST"),
	("spoke", "V", "0dp", "PT"),
	("speaking", "V", "0dp", "G"),
	("spoken", "V", "0p", "I"),
	("spoken", "V", "0dp", "N"),

	("grow", "V", "0dp", "R"),
	("grow", "V", "0dp", "P"),
	("grows", "V", "0dp", "S"),
	("grew", "V", "0dp", "ST"),
	("grew", "V", "0dp", "PT"),
	("growing", "V", "0dp", "G"),
	("grown", "V", "0p", "I"),
	("grown", "V", "0dp", "N"),

	("suggest", "V", "dcr", "R"),
	("suggest", "V", "dcr", "P"),
	("suggests", "V", "dcr", "S"),
	("suggested", "V", "dcr", "ST"),
	("suggested", "V", "dcr", "PT"),
	("suggested", "V", "0cr", "I"),
	("suggested", "V", "dcr", "N"),
	("suggesting", "V", "dcr", "G"),

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
	("ate", "V", "0dp", "ST"),
	("ate", "V", "0dp", "PT"),
]

# types of complements each head can have
selection_rules = {
	"V": "0dcpar",
	"I": "_",
	"N": "0",
	"D": "n",
	"P": "d",
	"NAME": "0",
	".": "0",
	"?": "0",
	"CC": "0",
	"SC": "ndv",
}

vocab_parameters = collections.defaultdict(str, {
	"V": "RSPGNTI",
	"I": "DPSV*%$HTM",
	"N": "SPOJ",
	"D": "SPOJ",
	"CC": "A",
})

carried_parameters = set(char for char in "m.?RSPGNTSCWOJ")

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
		for r in rule[1:]
		for char in r[1]
        if not (len(r) > 2 and r[2] == 0)
	}
	remaining_parameters = "".join(carried_parameters - used_parameters)
	return [
		(
			rule[0],
			gen_tag(rule[1][0], parameters + rule[1][1]),
			[
				gen_tag(r[0], ("" if len(r) > 2 and r[2] == 0 else parameters) + r[1])
				for r in rule[2:]
			]
		)
		for parameters in enumerate_parameters(remaining_parameters)
	]

def gen_vocab_rule(word, symbol, selection_parameters, parameters=""):
	return (1, gen_tag(symbol, "".join(sorted(c for c in selection_parameters + parameters))), (word,))

def gen_grammar(rules):
	grammar = [
		static_rule
		for rule in rules
		for static_rule in gen_rules(rule)
	] + [
		gen_vocab_rule(*word)
		for word in vocabulary
	] + [
		(1, "START", "S"),
		(1, "S", ("S_()",)),
	] + [
		(1, gen_tag(pos, p + vp), (gen_tag(pos, parameters + vp),))
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
			rule[1]
			for rule in grammar
			if all([
				r in terminatable
				for r in rule[2]
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
			for r in rule[2]
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
			#".1" if is_recursive(rule) else "1",
			"{:.12f}".format(rule[0]),
			rule[1],
			" ".join(rule[2]),
		)) for rule in grammar
	)

print(to_string(gen_grammar(rules)))

#pdb.set_trace()

