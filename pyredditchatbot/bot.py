"""
Bot class used for creating and running the bot
"""

import logging
import os
import re
import time
from typing import Sequence

import praw
import prawcore

from pyredditchatbot.exceptions import BotCredentialError, QuotesNotFoundError
from pyredditchatbot.utils import get_random_quote, default_cleaner

logger = logging.getLogger("pyredditchatbot")


class Bot:
    """
    Bot class used for creating and running the chatbot
    """

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            username: str,
            password: str,
            key_phrase: str,
            subreddit: str,
            quote_cleaner=None,
            user_agent=None,
            **praw_config
    ):
        """
        Initialize Bot instance

        :param client_id: ID of reddit application created.
        :param client_secret: Secret of reddit application created.
        :param username: Username of reddit account.
        :param password: Password of reddit account.
        :param subreddit: Subreddit in which the bot will run.
        :param key_phrase: Phrase to search for in comments. Bot will reply to each comment having
            this phrase.
        :param user_agent: User agent the bot will identify as.
        :param quote_cleaner: A callable that will pre-process your quotes before being saved into
            the Bot instance.
        :param praw_config: Further configurations that can be modified as per requirements.
            Check out https://praw.readthedocs.io/en/stable/getting_started/configuration.html for
            more details.
        """
        self.key_phrase = key_phrase
        self.username = username
        self.subreddit = subreddit

        if user_agent is None:
            self.user_agent = f"{username} Bot"
            logger.debug(f"No user agent supplied. Using user_agent - {self.user_agent}")
        else:
            self.user_agent = user_agent

        self.quote_cleaner = quote_cleaner or default_cleaner

        self._client = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=self.username,
            password=password,
            user_agent=self.user_agent,
            **praw_config
        )
        self.quotes = []

        self._subreddit_conn = self._client.subreddit(self.subreddit)

    def run(self):
        """
        Runs the bot.

        Will continue to run until terminated.
        """
        print("Running bot..Press Ctrl+c to terminate")

        # No quotes are configured
        # Check locally for quotes.txt
        if len(self.quotes) == 0:
            self._get_local_quotes()

        logger.info(f"Found {len(self.quotes)} quote(s)")
        try:
            # continuously streams comments and posts until manually broken
            for comment in self._subreddit_conn.stream.comments():
                if re.search(self.key_phrase, comment.body, re.IGNORECASE):
                    reply = get_random_quote(self.quotes)
                    logger.debug(f"Using quote - `{reply}`")

                    comment.reply(reply)
                    logger.info(
                        f"Replied to comment [{comment.id}] by u/{comment.author.name}"
                    )
                    # reddit APIs allow 1 request for every 2 seconds
                    time.sleep(3)
        # to catch case where subreddit value is invalid
        except prawcore.exceptions.Redirect as err:
            if str(err) == "Redirect to /subreddits/search":
                raise BotCredentialError(
                    f"Could not find subreddit - {self.subreddit}"
                )
        # to catch case where app credentials or user credentials are invalid
        except (prawcore.exceptions.ResponseException, prawcore.exceptions.OAuthException) as err:
            logger.error(f"Authentication failed - {err}")
            raise BotCredentialError(
                "Failed to connect with given credentials. Please verify credentials and their "
                "permissions."
            )

    def add_quotes(self, quotes: Sequence[str], clean: bool = True):
        """
        Add quotes to reddit instance

        :param quotes: Sequence of strings from which the bot chooses its replies.
        :param clean: Flag to pre-process the quotes supplied.
            if set to True, calls self.quote_cleaner on quotes and saves the output to the instance.
        """
        if clean:
            self.quotes = self.quote_cleaner(quotes)
        else:
            self.quotes = quotes

    def add_quotes_file(self, file_path: str, clean: bool = True):
        """
        Add quotes from a file to reddit instance.

        The contents of the file are separated by newline with each line being considered a new
        "quote".

        :param file_path: path to file from which quotes are read.
        :param clean: Flag to pre-process the quotes supplied.
            if set to True, calls self.quote_cleaner on quotes and saves the output to the instance.
        """
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                quotes = file.readlines()
        else:
            raise QuotesNotFoundError(f"Could not find quotes at {file_path}")

        self.add_quotes(quotes, clean)

    def _get_local_quotes(self):
        """
        Looks for quotes.txt in the current working directory.

        if present, adds to the bot instance.
        """
        temp_file_path = os.path.join(os.getcwd(), "quotes.txt")
        logger.debug(f"Looking for quotes.txt in {temp_file_path}")
        self.add_quotes_file(temp_file_path)
