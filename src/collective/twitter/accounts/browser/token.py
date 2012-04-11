# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from collective.twitter.accounts.config import ACCESS_TOKEN_URL
from collective.twitter.accounts.config import REQUEST_TOKEN_URL
from collective.twitter.accounts.config import AUTHORIZATION_URL

from collective.twitter.accounts.config import PLONE_CONSUMER_KEY
from collective.twitter.accounts.config import PLONE_CONSUMER_SECRET

from collective.twitter.accounts.config import PROJECTNAME

from urlparse import parse_qsl
import oauth2 as oauth
import logging

logger = logging.getLogger(PROJECTNAME)


class Validate(BrowserView):
    """
    View used to validate the provided token
    """

    def __call__(self,
                 consumer,
                 consumer_key,
                 consumer_secret,
                 oauth_token,
                 oauth_token_secret,
                 pincode):

        logger.info("Validate Twitter token.")
        logger.info("consumer=%s" % consumer)
        logger.info("consumer_key=%s" % consumer_key)
        logger.info("consumer_secret=%s" % consumer_secret)
        logger.info("oauth_token=%s" % oauth_token)
        logger.info("oauth_token_secret=%s" % oauth_token)
        logger.info("pincode=%s" % pincode)

        if consumer == "Plone default":
            consumer_key = PLONE_CONSUMER_KEY
            consumer_secret = PLONE_CONSUMER_SECRET

        # XXX: this seems not to be used
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        oauth_consumer = oauth.Consumer(key=consumer_key,
                                        secret=consumer_secret)

        token = oauth.Token(oauth_token, oauth_token_secret)
        token.set_verifier(pincode)

        oauth_client = oauth.Client(oauth_consumer, token)

        logger.info("OAuth client created.")

        resp, content = oauth_client.request(ACCESS_TOKEN_URL,
                                             method='POST',
                                             body='oauth_verifier=%s' % pincode)

        logger.info("Response: %s" % resp)
        access_token = dict(parse_qsl(content))

        if resp['status'] != '200':
            #ERROR
            return False
        else:
            #Success
            logger.info("Success! token: %s" % access_token)
            return access_token


class Request(BrowserView):
    """
    View used to generate a URL used to request a token to access a
    twitter account
    """

    def __call__(self, consumer, consumer_key=None, consumer_secret=None):
        logger.info("Request Twitter token.")
        logger.info("consumer=%s" % consumer)
        logger.info("consumer_key=%s" % consumer_key)
        logger.info("consumer_secret=%s" % consumer_secret)

        if consumer == "Plone default":
            consumer_key = PLONE_CONSUMER_KEY
            consumer_secret = PLONE_CONSUMER_SECRET

        if not consumer_key or not consumer_secret:
            return False

        # XXX: this seems not to be used
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        oauth_consumer = oauth.Consumer(key=consumer_key,
                                        secret=consumer_secret)

        oauth_client = oauth.Client(oauth_consumer)

        logger.info("Oauth client created, contacting Twitter")

        resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')

        logger.info("Response: %s" % resp)

        if resp['status'] != '200':
            #ERROR
            return False
        else:
            request_token = dict(parse_qsl(content))
            # XXX:
            # We return the URL needed to allow access to twitter, and we also
            # include the oauth_token and oauth_token_secret to be splitted
            # in Javascript. This is ugly.
            logger.info("URL to use: %s?oauth_token=%s" % (AUTHORIZATION_URL,
                                                request_token['oauth_token']))

            return '%s?oauth_token=%s&%s&%s' % (AUTHORIZATION_URL,
                                                request_token['oauth_token'],
                                                request_token['oauth_token'],
                                                request_token['oauth_token_secret'])
