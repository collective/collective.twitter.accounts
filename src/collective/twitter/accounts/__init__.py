  # -*- extra stuff goes here -*-

# Import PloneMessageFactory to create messages in the plone domain
from zope.i18nmessageid import MessageFactory
MessageFactory = MessageFactory('collective.twitter.accounts')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
