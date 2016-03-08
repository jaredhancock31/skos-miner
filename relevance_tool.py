import sys
import corpus_frequency
import thesaurus_related
from collections import OrderedDict


def main():
    relateds = thesaurus_related.get_relateds()
    frequencies = corpus_frequency.get_all_frequencies()
    relevance = {}

    for label, num_related in relateds.items():
        # print label, str(type(label))
        if label in frequencies:
            # sys.stdout.write(':)')
            freq = frequencies.get(label)   # get frequency from corpus list
            importance_score = round((0.3 * num_related) + (0.7 * freq), 4)
            relevance[label] = {'related': num_related, 'frequency': freq, 'importance': importance_score}
        # else:
        #     sys.stdout.write('~')

    # for i in relevance:
    #     imp = relevance.get(i)
    #     print i + ': ' + str(imp['importance'])

    ordered_rel = OrderedDict(sorted(relevance.iteritems(), reverse=True, key=lambda x: x[1]['importance']))
    # print ordered_rel['machine tool']

    for concept in ordered_rel:
        print concept + ": " + str(ordered_rel[concept]['importance'])


if __name__ == "__main__":
    main()