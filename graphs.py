from github import num_closed_of_each_label
import numpy as np

import matplotlib.pyplot as plt
plt.rcdefaults()

if __name__ == "__main__":
    # labels = ['e.1', 'e.2', 'e.4', 'e.8', 'e.16']
    labels = ['f-Admin','f-Courses', 'f-Comments', 'f-Submissions', 'f-Results', 'f-Profiles', 'f-Search', 'f-Email']
    num_closed_for = num_closed_of_each_label(labels)
    num_closed_by_index = []
    for label in labels:
        num_closed_by_index.append(num_closed_for[label])

    y_pos = np.arange(len(labels))

    plt.barh(y_pos, num_closed_by_index, align='center', alpha=0.4)
    plt.yticks(y_pos, labels)

    plt.show()