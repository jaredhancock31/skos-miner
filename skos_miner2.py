#!/usr/bin/env python


import thesaurus_related, corpus_frequency, skos_collect
from skos_collect import collect
from thesaurus_related import calc_related_scores
from constants import *
import sys


def main():
    thesaurus = collect()
    thesaurus, missing_concepts = calc_related_scores(thesaurus)

    for concept in thesaurus:
        print thesaurus[concept][PREF_LABEL], thesaurus[concept][IMPORTANCE_SCORE]


if __name__ == "__main__":
    main()
