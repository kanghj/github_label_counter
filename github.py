import re

from bs4 import BeautifulSoup
import requests
import time

from decorators import logging, memoize

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
        soup_of(
            'https://github.com/TEAMMATES/teammates/issues',
            'assignee:%s is:closed label:%s%s' % (_CONFIG['person'], str(_CONFIG['effort_prefix']), str(value),),
            1
        )
    ) * value


def num_closed_of_each_label(labels):
    result = {}
    for label in labels:
        result[label] = num_of_closed(
            soup_of(
                'https://github.com/TEAMMATES/teammates/issues',
                filter='assignee:%s label:%s' % (_CONFIG['person'], label, ),
                page=1
            )

        )
    return result


def names_of_assignables(assignee, milestones = None, *labels):
    if milestones is None:
        milestones = ['']
    return [map(
        lambda label: (
            names_of_assignable_in_soups(
                *soups_of(
                    'https://github.com/TEAMMATES/teammates/issues',
                    filter='assignee:%s label:%s milestone:%s' % (assignee, label, milestone)
                )

            )
        ),
        labels
    ) for milestone in milestones]


def numbers_of_assignables(assignee, milestones = None, *labels):

    return [map(
        lambda label: (
            numbers_of_assignable_in_soups(
                *soups_of(
                    'https://github.com/TEAMMATES/teammates/issues',
                    filter='assignee:%s label:%s milestone:%s' % (assignee, label, milestone)
                )
            )
        ),
        labels
    ) for milestone in milestones]


def soups_of(url, filter):
    print url
    print filter
    num_pages = num_of_closed(
        soup_of(url, filter, 1)
    ) // 25 + 1  # + 1 for leftovers

    return [soup_of(url, filter, i) for i in range(1, num_pages + 1)]


@memoize
def soup_of(url, filter, page):
    print 'soup of ', url, filter, page
    time.sleep(15)

    return BeautifulSoup(
        requests.get(
            url,
            params={
                'q': filter,
                'page': page,
            }
        ).text
    )


def numbers_of_assignable_in_soups(*soups):
    result = []
    for soup in soups:
        result.extend(numbers_of_assignable_in_soup(soup))
    return result


def numbers_of_assignable_in_soup(soup):
    try:
        return map(
            lambda metatext: extract_assignable_number(
                metatext.findAll('span')[0].getText().strip()
            ),
            soup.findAll('div', class_="issue-meta")
        )
    except IndexError:
        """
        No assignables on page
        """
        return ['']


def names_of_assignable_in_soups(*soups):
    result = []
    for soup in soups:
        result.extend(names_of_assignable_in_soup(soup))

    print "res is"
    print result
    return result



def names_of_assignable_in_soup(soup):
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
    return int(re.search('([0-9]*)', text).group(1))


def extract_assignable_number(text):
    return text.split()[0]

if __name__ == "__main__":
    print total_effort([1,2,4,8,16])

