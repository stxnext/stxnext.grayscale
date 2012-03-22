# -*- coding:utf-8 -*-
from zope.schema import TextLine, Choice, Tuple
from zope.component import adapts
from zope.interface import Interface, implements
from zope.formlib.form import FormFields

from Products.CMFDefault.formlib.schema import SchemaAdapterBase, ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.site import SiteControlPanel, SiteControlPanelAdapter
from plone.app.controlpanel.form import ControlPanelForm

#from stxnext.grayscale import VPMessageFactory as _

class IGrayscaleSettingsSchema(Interface):
    """Interface for additional control panel settings
    """

    transformed_themes = Tuple(title=u'Choice field',
                              description=u'desc',
                              required=False,
                              value_type=Choice(title=u'Choice field',
                                description=u'OPIS',
                                required = False,
                                vocabulary = 'plone.app.vocabularies.Skins')
                              )

class GrayscaleControlPanelAdapter(SiteControlPanelAdapter):
    """Adapter for greyscale site control panel.
    """

    adapts(IPloneSiteRoot)
    implements(IGrayscaleSettingsSchema)

    transformed_themes = ProxyFieldProperty(IGrayscaleSettingsSchema['transformed_themes'])


class GrayscaleSettingsForm(ControlPanelForm):
    """Static export form
    """

    form_fields = FormFields(IGrayscaleSettingsSchema)

    label = "Grayscale settings"
    description = None
    form_name = "Grayscale settings"
