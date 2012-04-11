# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.component import getUtility

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from plone.fieldsets.form import FieldsetsEditForm

from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.interface import alsoProvides

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from interfaces import ITwitterControlPanel

from collective.twitter.accounts import MessageFactory as _
from plone.registry.interfaces import IRegistry

from collective.twitter.accounts.config import PLONE_CONSUMER_KEY
from collective.twitter.accounts.config import PLONE_CONSUMER_SECRET

from collective.twitter.accounts.config import PROJECTNAME

from zope.component import getMultiAdapter

from zope.schema.interfaces import IContextSourceBinder

import logging

logger = logging.getLogger(PROJECTNAME)

consumer_vocabulary = SimpleVocabulary.fromValues([_(u"Plone default"), _(u"Custom")])


def make_terms(items):
    """ Create zope.schema terms for vocab from tuples """
    terms = [SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
             for pair in items]
    return terms


def TwitterApplications(context):

    app_list = [("Plone default", _(u"Plone default")),
                ("Custom", _(u"Custom"))]

    return SimpleVocabulary(make_terms(app_list))


alsoProvides(TwitterApplications, IContextSourceBinder)


class ITwitterFieldSchema(Interface):
    """ Twitter Config """
    consumer = schema.Choice(title=_(u'Application'),
                             description=_(u"Choose to use Plone's default "
                                            "tweet application or your own "
                                            "(you'll need to register one in "
                                            "dev.twitter.com)"),
                             required=True,
                             default="Plone default",
                             source=TwitterApplications)

    consumer_key = schema.TextLine(title=_(u'Consumer Key'),
                                   description=_(u"Consumer key for your "
                                                  "application. Not used if "
                                                  "\"Plone default\" chosen."),
                                   required=False)

    consumer_secret = schema.TextLine(title=_(u'Consumer Secret'),
                                      description=_(u"Consumer secret for your "
                                                     "application. Not used if "
                                                     "\"Plone default\" chosen."),
                                      required=False)

    oauth_token = schema.TextLine(required=False)

    oauth_token_secret = schema.TextLine(required=False)

    pincode = schema.TextLine(title=_(u'Token'),
                              description=_(u'Security token'),
                              required=True)


class TwitterControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ITwitterFieldSchema)

    consumer = ""
    consumer_key = ""
    consumer_secret = ""
    oauth_token = ""
    oauth_token_secret = ""
    pincode = ""


class TwitterControlPanel(FieldsetsEditForm):
    """
    Twitter control panel view
    """

    implements(ITwitterControlPanel)

    template = ViewPageTemplateFile('./templates/twitter-control-panel.pt')

    label = _("Twitter setup")
    description = _("""Lets you configure several twitter accounts""")
    form_name = _("Twitter setup")
    form_fields = form.FormFields(ITwitterFieldSchema)
    request_twitter_token = _(u"Request twitter token")

    def getAccounts(self):
        registry = getUtility(IRegistry)
        accounts = registry['collective.twitter.accounts']

        return accounts

    @form.action(_(u'label_add', default=u'Add'), name=u'add')
    def handle_add_action(self, action, data):
        logger.info("Adding account to the registry")
        consumer = data['consumer']
        consumer_key = data['consumer_key']
        consumer_secret = data['consumer_secret']
        oauth_token = data['oauth_token']
        oauth_token_secret = data['oauth_token_secret']
        pincode = data['pincode']

        if consumer == "Plone default":
            consumer_key = PLONE_CONSUMER_KEY
            consumer_secret = PLONE_CONSUMER_SECRET

        if (consumer_key and
            consumer_secret and
            oauth_token and
            oauth_token_secret and
            pincode):

            validate_token = getMultiAdapter((self.context, self.request),
                                             name='validate-token')

            access_token = validate_token(consumer, consumer_key, consumer_secret,
                                          oauth_token, oauth_token_secret, pincode)

            if access_token:

                registry = getUtility(IRegistry)
                accounts = registry['collective.twitter.accounts']
                if not accounts:
                    accounts = {}

                username = access_token['screen_name']
                oauth_token = access_token['oauth_token']
                oauth_token_secret = access_token['oauth_token_secret']

                accounts[username] = \
                                     {'consumer_key': consumer_key,
                                      'consumer_secret': consumer_secret,
                                      'oauth_token': oauth_token,
                                      'oauth_token_secret': oauth_token_secret}

                registry['collective.twitter.accounts'] = accounts

                logger.info("Account added succesfully to the registry")

                logger.info("Token: %s" % access_token)
                self.status = _("Twitter account succesfully authorized.")

            else:
                logger.info("Account was not added to the registry")
                self.status = _("Could not authorize. Perhaps wrong token provided.")
        else:
            self.status = _("Missing data.")


class RemoveAuthAccount(BrowserView):

    def __call__(self, account_name):
        registry = getUtility(IRegistry)
        accounts = registry['collective.twitter.accounts']
        if not accounts:
            accounts = {}

        try:
            del accounts[account_name]
        except:
            pass
