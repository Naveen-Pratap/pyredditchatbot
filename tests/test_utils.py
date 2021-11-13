from unittest import TestCase

from pyredditchatbot.utils import default_cleaner, get_random_quote


class TestGetRandomQuote(TestCase):
    def test_get_random_quote(self):
        quotes = [
            "hello",
            "foo",
            "bar"
        ]

        quote = get_random_quote(quotes)

        assert quote in quotes
        assert isinstance(quote, str)


class TestDefaultCleaner(TestCase):
    def test_remove_empty(self):
        quotes = [
            "hello",
            "",
            "bar"
        ]

        output = default_cleaner(quotes)

        assert len(output) == 2
        assert "" not in output
