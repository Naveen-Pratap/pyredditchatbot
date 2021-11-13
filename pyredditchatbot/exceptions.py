"""
Pyredditchatbot exception classes
"""


class QuotesNotFoundError(Exception):
    """
    Raised when Quotes are not be discovered correctly.
    """
    pass


class BotCredentialError(Exception):
    """
    Raised for any authorisation/authentication error raised by PRAW.
    """
    pass
