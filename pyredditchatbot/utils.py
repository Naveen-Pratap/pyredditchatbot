import random

# TODO: Typing to sequence
def get_random_quote(
        quotes: list
) -> str:
    """
    :rtype: str
    :param
        quotes: list of quotes from which a random quote is to be selected
    :return:
        A randomly selected quote
    """
    return random.choice(quotes)


def default_cleaner(quotes):
    quotes = [q.strip() for q in quotes if q]
    return quotes
