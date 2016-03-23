"""
    Author: Jared Hancock
    Date: March 2016
    Email: jaredhancock31@gmail.com
"""
import corpus_frequency
import thesaurus_related
import sys


def normalize_on_max(merged_list, max_score):
    sys.stdout.write("normalizing results.....")
    for concept in merged_list:
        merged_list[concept]['score'] = round(float(merged_list[concept]['score'] / max_score), 4)
    print 'done.'
    return merged_list


def main():
    related_list = thesaurus_related.get_relateds()
    frequency_list = corpus_frequency.get_all_frequencies()
    merged_list = {}        # houses union of all sets, overall importance scores

    total_imp = 0
    max_score = 0

    for label, num_related in related_list.items():
        score = round((0.3 * num_related), 4)
        total_imp += score

        merged_list[label] = {'related': num_related, 'freq': None, 'score': score}

        max_score = max(score, max_score)   # update highest score

    for label, freq in frequency_list.items():
        score = round((0.7 * freq), 4)
        total_imp += score

        if label in merged_list:
            merged_list[label]['freq'] = freq
            merged_list[label]['score'] += score
            max_score = max(max_score, merged_list[label]['score'])
        else:
            merged_list[label] = {'related': None, 'freq': freq, 'score': score}
            max_score = max(max_score, score)

    # print "max score: " + str(max_score)
    merged_list = normalize_on_max(merged_list, max_score)

    print
    print("\n========================================RESULTS============================================")

    for concept in sorted(merged_list, key=merged_list.get, reverse=True):
        print '{0:80}' '{1:.3f}'.format(concept, merged_list[concept]['score'])

if __name__ == "__main__":
    main()
