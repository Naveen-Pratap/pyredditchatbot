"""
Utility functions for  pyredditchatbot
"""

import random

# TODO: Typing to sequence
def get_random_quote(
        quotes
):
    """
    Gets a random quote from a sequence of quotes.

    :param
        quotes: Sequence of quotes from which a random quote is to be selected.
    :return:
        A randomly selected quote.
    """
    return random.choice(quotes)


def default_cleaner(quotes):
    """
    Default cleaner function used by bot instance.

    :param quotes: Sequence of quotes which are to be pre-processed.
    :return:
        processed quotes.
    """
    quotes = [q.strip() for q in quotes if q]
    return quotes
