import os.path
from unittest import TestCase, mock

import praw.models
import prawcore
import requests

from pyredditchatbot import Bot
from pyredditchatbot.exceptions import BotCredentialError, QuotesNotFoundError


class TestAddQuote(TestCase):
    def setUp(self) -> None:
        self.bot = Bot(
            "test_client_id",
            "test_client_secret",
            "test_username",
            "test_password",
            "u/test",
            "test_subreddit"
        )

    def test_add_quotes_dirty(self):
        """
        Add quotes with clean=False
        """
        quotes = [
            "hello",
            "",
            "foo"
        ]

        self.bot.add_quotes(quotes, clean=False)
        assert self.bot.quotes == quotes


class TestAddQuoteFile(TestCase):
    def setUp(self) -> None:
        self.bot = Bot(
            "test_client_id",
            "test_client_secret",
            "test_username",
            "test_password",
            "u/test",
            "test_subreddit"
        )

    @mock.patch.object(os.path, 'exists')
    def test_add_quotesfile_exception_on_invalid_file(self, m_exists):
        file_path = "a/nonexistent/path"
        m_exists.return_value = False

        self.assertRaises(QuotesNotFoundError, self.bot.add_quotes_file, file_path, clean=False)


class TestRun(TestCase):
    def setUp(self) -> None:
        self.bot = Bot(
            "test_client_id",
            "test_client_secret",
            "test_username",
            "test_password",
            "u/test",
            "test_subreddit"
        )

    @mock.patch.object(praw.models.reddit.subreddit.SubredditStream, 'comments')
    def test_run_raise_error_on_invalid_creds(self, m_stream):
        response_mock = mock.MagicMock()
        type(response_mock).status_code = mock.PropertyMock(return_value=401)
        m_stream.side_effect = prawcore.exceptions.ResponseException(response_mock)
        self.bot.quotes = ["test"]
        self.assertRaises(BotCredentialError, self.bot.run)

    @mock.patch.object(praw.models.reddit.subreddit.SubredditStream, 'comments')
    def test_run_raise_error_on_invalid_subreddit(self, m_stream):
        response_mock = mock.MagicMock()
        type(response_mock).headers = mock.PropertyMock(
            return_value={"location": "/subreddits/search"}
            )
        m_stream.side_effect = prawcore.exceptions.Redirect(response_mock)
        self.bot.quotes = ["test"]
        self.assertRaises(BotCredentialError, self.bot.run)
