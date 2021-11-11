import logging
import os
import re
import time

import praw

from utils import get_random_quote, default_cleaner

logger = logging.getLogger("__name__")


class QuotesNotFoundError(Exception):
    pass


class Bot:
    def __init__(
            self,
            client_id,
            client_secret,
            username,
            password,
            subreddit,
            key_phrase,
            user_agent=None,
            quote_cleaner=None,
            **praw_config
    ):
        self.key_phrase = key_phrase
        self.username = username
        self.subreddit = subreddit

        if user_agent is None:
            user_agent = "{} Bot".format(username)
            logger.debug("No user agent supplied. Using user_agent - {}".format(user_agent))

        if quote_cleaner is None:
            self.quote_cleaner = default_cleaner

        self._client = praw.Reddit(
            client_id,
            client_secret,
            username,
            password,
            user_agent,
            **praw_config
        )
        self.quotes = []

        self._subreddit_conn = self._client.subreddit(self.subreddit)

    def run(self):
        print("Running bot..Press Ctrl+c to terminate")
        # continuously streams comments and posts until manually broken
        for comment in self._subreddit_conn.stream.comments():
            if re.search(self.key_phrase, comment.body, re.IGNORECASE):

                if len(self.quotes) == 0:
                    temp_file_path = os.path.join(os.getcwd(), "quotes.txt")
                    logger.debug("Looking for quotes.txt in {}".format(temp_file_path))
                    if os.path.exists(temp_file_path):
                        self.add_quotes_file(temp_file_path)
                    else:
                        raise QuotesNotFoundError("Found 0 quotes. Did you forget to add them?")

                logger.info("Found {} quotes".format(len(self.quotes)))
                reply = get_random_quote(self.quotes)
                logger.debug("Using quote - `{}`".format(reply))

                comment.reply(reply)
                logger.info(
                    "Replied to comment [{}] by u/{}".format(comment.id, comment.author.name)
                )
                # reddit APIs allow 1 request for every 2 seconds
                time.sleep(3)

    def add_quotes(self, quotes, clean=True):
        if clean:
            self.quotes = [self.quote_cleaner(q) for q in quotes]
        else:
            self.quotes = quotes

    def add_quotes_file(self, file_path, clean=True):
        if os.path.exists(file_path):
            with open("quotes.txt", "r") as file:
                quotes = file.readlines()

        self.add_quotes(quotes)
