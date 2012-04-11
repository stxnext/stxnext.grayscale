# -*- coding: utf-8 -*-
import logging
from zope.i18nmessageid import MessageFactory

log = logging.getLogger('stxnext.grayscale')
StxnextGrayscaleMessageFactory = MessageFactory('stxnext.grayscale')

def initialize(context):
    """
    Initializer called when used as a Zope 2 product.
    """
