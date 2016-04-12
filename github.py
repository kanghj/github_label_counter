
from bs4 import BeautifulSoup
import requests

from decorators import logging

_CONFIG = {
    'person': 'kanghj',
    'effort_prefix': 'e.',
}


def total_effort(labels):
    return sum( 
        (total_numerical_value_of(label) for label in labels)
    )


@logging
def total_numerical_value_of(value):
    return num_of_closed(
        BeautifulSoup(
            requests.get(
                'https://github.com/TEAMMATES/teammates/issues',
                params={
                    'q': 'assignee:%s is:closed label:%s%s' %
                         (_CONFIG['person'], str(_CONFIG['effort_prefix']), str(value),)
                }
            ).text
        )
    ) * value


def num_closed_of_each_label(labels):
    result = {}
    for label in labels:
        result[label] = num_of_closed(
            BeautifulSoup(
                requests.get(
                    'https://github.com/TEAMMATES/teammates/issues',
                    params={
                        'q': 'assignee:%s label:%s' %
                             (_CONFIG['person'], label, )
                    }
                ).text
            )
        )
    return result


def names_of_assignables_of_labels_and_assignee(assignee, *labels):
    soup = BeautifulSoup(
        requests.get(
            'https://github.com/TEAMMATES/teammates/issues',
            params={
                'q': 'assignee:%s label:%s' %
                     (_CONFIG['person'], label,)
            }
        ).text
    )
    return map(
        lambda label: (
            numbers_of_assignable(
                soup
            ),
            names_of_assignable(
                soup
            )
        ),
        labels
    )


def numbers_of_assignable(soup):
    return map(
        lambda metatext: extract_number(metatext),
        soup.findAll('span', class_="issue-meta")
    )


def names_of_assignable(soup):
    return map(
        lambda link: link.getText().strip(),
        soup.findAll('a', class_="issue-title-link")
    )


def num_of_closed(soup):
    return extract_number(
        closed_prs_button(soup).getText()
                               .strip()
    ) 


def num_of_open(soup):
    return extract_number(
        opened_prs_button(soup).getText()
                               .strip()
    )


def closed_prs_button(soup):
    return button_with_word(soup, 'Closed')


def opened_prs_button(soup):
    return button_with_word(soup, 'Open')


def button_with_word(soup, word):
    return filter(
        lambda selected_link: word in selected_link.getText(),
        soup.findAll('a', class_="btn-link")
    )[0]


def extract_number(text):
    import re
    return int(re.search('([0-9]*)', text).group(1))

if __name__ == "__main__":
    print total_effort([1,2,4,8,16])
