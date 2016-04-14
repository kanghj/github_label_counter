from itertools import izip

from github import total_effort, names_of_assignables, numbers_of_assignables
from stopwords import stopwords
import string

import re


def assignable_short_name(assignable):
    assignable = assignable.lower()
    for punct in string.punctuation:
        assignable = assignable.replace(punct, '-')
    for stopword in stopwords:
        assignable = assignable.replace(' ' + stopword + ' ', ' ')
    assignable = assignable.replace(' ', '-')

    assignable = re.sub('[\w]{10,}', '-', assignable)

    return re.sub('-+', '-', assignable)


if __name__ == "__main__":
    labels = ['e.1','e.2', 'e.4', 'e.8', 'e.16']

    names = names_of_assignables(
        'kanghj', *labels
    )
    print names

    numbers = numbers_of_assignables(
        'kanghj', *labels
    )
    print numbers

    value_of_labels = {
        'e.1': 1,
        'e.2': 2,
        'e.4': 4,
        'e.8': 8,
        'e.16': 16,
    }

    bin_size = 16
    bins = []
    bin_label_value = []

    for label_index, (assignable_names, assignable_numbers) in enumerate(izip(names, numbers)):
        print len(assignable_names)
        name_iter = iter(assignable_names)
        number_iter = iter(assignable_numbers)

        label_value = value_of_labels[labels[label_index]]
        num_things_in_bin = bin_size // label_value
        try:
            while True:
                bin = []
                bin_label_value.append(label_value)
                for i in xrange(num_things_in_bin):
                    assignable_name = next(name_iter)
                    number = next(number_iter)
                    print label_value, assignable_name, number

                    bin.append(
                        (assignable_name, number)
                    )
                bins.append(bin)

        except StopIteration:
            bins.append(bin)

    for bin_label, bin in izip(bin_label_value, bins):
        print_just_number = len(bin) >= 8
        for name, number in bin:
            if print_just_number:
                print str(bin_label) + 'h:' + number + ', ',
            else:
                print str(bin_label) + 'h:' + number + '-' + assignable_short_name(name) + ', ',

        print ''
        print '----'

