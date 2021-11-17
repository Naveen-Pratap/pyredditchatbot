Pyredditchatbot
===================================

Pyredditchatbot is a Python package for easily building reddit chatbots that surf your favourite subreddit and replies
when called. Simply modify the parameters mentioned in the Quickstart to create your own custom reddit chatbot to add
some life to your subreddit!


Installation
------------

Pyredditchatbot is supported on Python 3.7 and above. The recommended way to install it is via `pip
<https://pypi.python.org/pypi/pip>`.

    pip install pyredditchatbot

For instructions on installing Python and pip see "The Hitchhiker's Guide to Python"
`Installation Guides <https://docs.python-guide.org/en/latest/starting/installation/>`.

Quickstart
----------

Go to  https://www.reddit.com/prefs/apps/ and login with your reddit account. This is the account that will be replying, so
consider making a new account if you're looking to roleplay as a character. Please also make sure to read
reddit etiquette and guidelines before creating a bot.

Create a script type application by filling out the form. You should now have a client id and secret for the application
just created.

You can create a bot like so:

    import pyredditchatbot as prc

    bot = prc.Bot(
        client_id,
        client_secret,
        reddit_username,
        reddit_password,
        "u/my-bot",
        "my-favourite-subreddit"
    )

The bot surfs all the comments on the subreddit `my-favourite-subreddit`
and replies whenever it sees the phrase `u/my-bot` in a comment.

You need to add quotes to your bot to help it choose what to reply with. By default it looks for `quotes.txt` locally.
You can also add your quotes as an iterable like this:

    quotes = ["Hi", "How are you!!", "Hello!"]
    bot.add_quotes(quotes)

You can also fetch quotes directly from a file:

    bot.add_quotes_file("path/to/file/quotes.txt")

Each new line in the file is considered as a new quote.

If you want to pre_process the quotes, you can pass your custom callable like so:

    bot = prc.Bot(
        client_id,
        client_secret,
        username,
        password,
        "u/my-bot",
        "my-favourite-subreddit"
        quote_cleaner=my_pre_processor_func
    )

This will call `my_pre_processor_func(quotes)` and add the output to the bot instance.

If no quote_cleaner is passed, a default cleaner which simple removes empty quotes is used.

To run the bot, simply do:

    bot.run()

This will run the bot continuously until the script is terminated.

If the bot is run without any quotes and a local `quotes.txt`
doesn't exist, the run fails with a `QuotesNotFoundError`.

License
-------

Pyredditchatbot is provided under the `Simplified BSD License`
