===========================
collective.twitter.accounts
===========================

.. contents:: Table of Contents

Overview
--------

This product allows you to add Twitter_ accounts to a Plone site.

It uses oAuth authentication.

Usage
-----

- Go to the "Site Setup", then to the "Twitter" tool.
- Choose wether to use Plone's default twitter application (PloneTweet) or a
  custom one.
- If you choose to use a custom Twitter application, enter your consumer key
  and secret for it.
- Click on "Request Twitter token".
- A new link should've appeared below "Allow permission to your account".
  Click it in order to allow the app to use your Twitter account.
- Copy the given token into the "Token" input field.
- Click "Add".
- If something went wrong, you need to click on "Request Twitter token" and
  the following link to get a new token and try again.

Done.

If you want to remove an account, simply click on its red cross next to its
name. Be carefull, it will delete the account without confirmation, and it
cannot be undone.

Twitter Applications
--------------------

In order to allow external access to a twitter account, you need to register
an "Application" in https://dev.twitter.com/ There's already a "PloneTweet"
application registered that can be used, but if you want to use your own, just
regiter it there.

Actually posting or getting to/from Twitter
-------------------------------------------

This product just saves the needed data in order to post tweets or read them.
You'll need additional products in order to do so, for example
`collective.twitter.action`_ or `collective.twitter.portlets`_.

.. _`collective.twitter.action`: http://pypi.python.org/pypi/collective.twitter.action
.. _`collective.twitter.portlets`: http://pypi.python.org/pypi/collective.twitter.portlets
.. _Twitter: http://twitter.com/

