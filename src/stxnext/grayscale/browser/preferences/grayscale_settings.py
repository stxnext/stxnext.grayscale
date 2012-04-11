# -*- coding:utf-8 -*-
from zope.schema import TextLine, Choice, Tuple
from zope.component import adapts
from zope.interface import Interface, implements
from zope.formlib.form import FormFields

from Products.CMFDefault.formlib.schema import SchemaAdapterBase, ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.site import SiteControlPanel, SiteControlPanelAdapter
from plone.app.controlpanel.form import ControlPanelForm

from stxnext.grayscale import StxnextGrayscaleMessageFactory as _

class IGrayscaleSettingsSchema(Interface):
    """
    Interface for additional control panel settings
    """

    transformed_themes = Tuple(title = _(u'Skins transformed to grayscale'),
                               description = _(u'Select skin to be transformed to grayscale'),
                               required = False,
                               value_type = Choice(required = False,
                                                   vocabulary = 'plone.app.vocabularies.Skins')
                               )

class GrayscaleControlPanelAdapter(SiteControlPanelAdapter):
    """
    Storage for grayscale site control panel settings
    """

    adapts(IPloneSiteRoot)
    implements(IGrayscaleSettingsSchema)

    transformed_themes = ProxyFieldProperty(IGrayscaleSettingsSchema['transformed_themes'])


class GrayscaleSettingsForm(ControlPanelForm):
    """
    Grayscale transformation skins settings form
    """

    form_fields = FormFields(IGrayscaleSettingsSchema)

    label = _('Grayscale settings')
    description = ''
    form_name = _('Grayscale skin settings')
