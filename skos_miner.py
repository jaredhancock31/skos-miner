#!/usr/bin/env python
"""
    Author: Jared Hancock
    Date: April 2016
    Email: jaredhancock31@gmail.com
"""

import thesaurus_related, corpus_frequency, skos_collect
from skos_collect import collect
from collections import OrderedDict
from constants import *
import corpus_frequency
import thesaurus_related
import operator
import sys


def normalize_on_max(thesaurus, my_max=None):
    if my_max is not None:
        for concept in thesaurus:
            prev_score = thesaurus[concept][IMPORTANCE_SCORE]
            thesaurus[concept][IMPORTANCE_SCORE] = round(prev_score / my_max, 4)
    return thesaurus


def normalize_on_sum(thesaurus, total=None):
    if total is not None:
        for concept in thesaurus:
            prev_score = thesaurus[concept][IMPORTANCE_SCORE]
            thesaurus[concept][IMPORTANCE_SCORE] = round(prev_score / total, 4)
    return thesaurus


def main(rdf_file):

    if rdf_file is not None:
        thesaurus = collect(rdf_file)
        if '.rdf' not in rdf_file[-4:]:
            sys.stderr.write('File inputted needs to be an .rdf file.')
            return
    # default test file TODO remove before release
    else:
        thesaurus = collect("res/pp_project_manuterms.rdf")

    thesaurus, missing_concepts = thesaurus_related.calc_related_scores(thesaurus)
    thesaurus.update(missing_concepts)

    # thesaurus, missing_concepts = corpus_frequency.get_corpus_data(thesaurus)
    # thesaurus.update(missing_concepts)
    freq_data = corpus_frequency.get_corpus_data()

    total_imp = 0

    for concept in thesaurus:
        label = thesaurus[concept][PREF_LABEL].lower()

        if label in freq_data:
            freq = freq_data[label]
            thesaurus[concept][FREQUENCY] = freq
            thesaurus[concept][IMPORTANCE_SCORE] += (freq * FREQ_SCORE_FACTOR)
            total_imp += thesaurus[concept][IMPORTANCE_SCORE]
            freq_data.pop(label)

    # if there are some concept left over from the corpus side, add them in. These are probably foreign concepts
    # with weird encodings in the URIs. TODO Scrub the data so that these are matched with their thesaurus counterparts
    if any(freq_data):
        for label in freq_data:
            freq = freq_data[label]
            score = (freq * FREQ_SCORE_FACTOR)
            thesaurus['corpus-'+label] = {PREF_LABEL: label,
                                          FREQUENCY: freq,
                                          NUM_RELATIONS: 0,
                                          NUM_EXTERNAL: 0,
                                          IMPORTANCE_SCORE: score,
                                          }
            total_imp += score

    max_score = max(float(d[IMPORTANCE_SCORE]) for d in thesaurus.values())

    print ("Normalizing values.......\n")
    # thesaurus = normalize_on_sum(thesaurus, total_imp)
    thesaurus = normalize_on_max(thesaurus, max_score)
    thesaurus = OrderedDict(sorted(thesaurus.items(), key=lambda t: t[1][IMPORTANCE_SCORE], reverse=True))

    # print column headers
    print "{:<80} {:<10} {:<10} {:<10} {:<10}".format("Label",
                                                      "Frequency",
                                                      "Relations",
                                                      "Externals",
                                                      "Importance")
    print "{:<110}".format("-"*125)
    for concept in thesaurus:
        print "{:<80} {:<10} {:<10} {:<10} {:<10}".format(thesaurus[concept][PREF_LABEL][:40],
                                                   thesaurus[concept][FREQUENCY],
                                                   thesaurus[concept][NUM_RELATIONS],
                                                   thesaurus[concept][NUM_EXTERNAL],
                                                   thesaurus[concept][IMPORTANCE_SCORE])


if __name__ == "__main__":
    main('res/pp_project_manuterms.rdf')
    # main(sys.argv)
