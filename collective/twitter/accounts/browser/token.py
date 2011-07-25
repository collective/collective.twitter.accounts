from Products.Five import BrowserView
from zope.component import getUtility

from collective.twitter.accounts.config import ACCESS_TOKEN_URL
from collective.twitter.accounts.config import REQUEST_TOKEN_URL
from collective.twitter.accounts.config import AUTHORIZATION_URL

from collective.twitter.accounts.config import PLONE_CONSUMER_KEY
from collective.twitter.accounts.config import PLONE_CONSUMER_SECRET

from urlparse import parse_qsl
import oauth2 as oauth

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
    
    
        if consumer == "Plone default":
            consumer_key = PLONE_CONSUMER_KEY
            consumer_secret = PLONE_CONSUMER_SECRET
 
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        oauth_consumer = oauth.Consumer(key=consumer_key, 
                                        secret=consumer_secret)
    
        token = oauth.Token(oauth_token, oauth_token_secret)
        token.set_verifier(pincode)
    
        oauth_client  = oauth.Client(oauth_consumer, token)
        resp, content = oauth_client.request(ACCESS_TOKEN_URL, 
                                             method='POST', 
                                             body='oauth_verifier=%s' % pincode)
        access_token  = dict(parse_qsl(content))
    
        if resp['status'] != '200':
            #ERROR
            return False
        else:
            #Success
            return access_token


class Request(BrowserView):
    """
    View used to generate a URL used to request a token to access a 
    twitter account
    """
    
    def __call__(self, consumer, consumer_key=None, consumer_secret=None):

        if consumer == "Plone default":
            consumer_key = PLONE_CONSUMER_KEY
            consumer_secret = PLONE_CONSUMER_SECRET
    
        if not consumer_key or not consumer_secret:
            return False
    
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        oauth_consumer = oauth.Consumer(key=consumer_key, 
                                        secret=consumer_secret)
 
        oauth_client = oauth.Client(oauth_consumer)

        resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')

        if resp['status'] != '200':
            #ERROR
            return False
        else:
            request_token = dict(parse_qsl(content))
            # XXX:
            # We return the URL needed to allow access to twitter, and we also
            # include the oauth_token and oauth_token_secret to be splitted
            # in Javascript. This is ugly.
            return '%s?oauth_token=%s&%s&%s' % (AUTHORIZATION_URL, 
                                                request_token['oauth_token'],
                                                request_token['oauth_token'],
                                                request_token['oauth_token_secret'])