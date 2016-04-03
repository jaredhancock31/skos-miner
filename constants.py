#!/usr/bin/env python

REL_SCORE_FACTOR = 0.3
FREQ_SCORE_FACTOR = 0.7
EXTERNAL_LINK_FACTOR = 0.1
IMPORTANCE_SCORE = 'importance'
PREF_LABEL = 'prefLabel'
RELATEDS = 'relateds'
NUM_RELATIONS = 'num_relations'
FREQUENCY = 'frequency'
EXACT_MATCH = 'exactMatch'
CLOSE_MATCH = 'closeMatch'
BROADER_MATCH = 'broaderMatch'
NARROWER_MATCH = 'narrowerMatch'
RELATED_MATCH = 'relatedMatch'

EXTERNAL_PROPERTIES = [EXACT_MATCH,
                       CLOSE_MATCH,
                       BROADER_MATCH,
                       NARROWER_MATCH,
                       RELATED_MATCH]
