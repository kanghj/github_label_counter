from itertools import izip

from github import total_effort, names_of_assignables_of_labels_and_assignee


if __name__ == "__main__":
    labels = ['e.1', 'e.2', 'e.4', 'e.8', 'e.16']
    assignables = names_of_assignables_of_labels_and_assignee(
        'kanghj', *labels
    )

    value_of_labels = {
        'e.1': 1,
        'e.2': 2,
        'e.4': 4,
        'e.8': 8,
        'e.16': 16,
    }

    bin_size = 16
    bins = []

    for label_index, assignable_names in enumerate(assignables):
        name_iter = iter(assignable_names)
        bin = []

        label_value = value_of_labels[labels[label_index]]
        num_things_in_bin = bin_size // label_value

        for i in xrange(num_things_in_bin):
            try:
                bin.append(
                    next(name_iter)
                )
            except StopIteration:
                break

        bins.append(bin)

    for i, bin in enumerate(bins):
        print i, bin
        print len(bin)
