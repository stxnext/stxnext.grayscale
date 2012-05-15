from Acquisition import aq_base
from OFS.Image import File
from Products.CMFCore.FSFile import FSFile
from Products.CMFCore.FSImage import FSImage
from Products.ATContentTypes.interface.image import IATImage
from Products.ATContentTypes.content.file import ATFile
from plone.app.linkintegrity.interfaces import IOFSImage
from zope.publisher.interfaces.browser import IBrowserView
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.FSPageTemplate import FSPageTemplate

try:
    from plone.resource.file import FilesystemFile
    PLONE_RESOURCE_INSTALLED = True
except ImportError:
    PLONE_RESOURCE_INSTALLED = False

from stxnext.grayscale import log
import utils

def transformation_event(event):
    """
    Checks if current default theme is 
    meant to be transformed to grayscale
    """
    request = event.request
    try:
        portal = getUtility(ISiteRoot)
    except ComponentLookupError:
        return
    skins_tool = getToolByName(portal, 'portal_skins')
    properties_tool = getToolByName(portal, 'portal_properties')
    transformed_themes = properties_tool.site_properties.getProperty('transformed_themes')
    if not transformed_themes:
        return
    request_varname = skins_tool.request_varname
    if request.get(request_varname):
        selected_skin = request.get(request_varname)
    else:
        selected_skin = skins_tool.getDefaultSkin()
    if selected_skin in transformed_themes:
        GrayscaleTransformations(event)


#def failure_event(event):
#    """
#    """
#    parent = event.request.get('PARENTS')[0]
#    if parent:
#        path = event.request.other['VIRTUAL_URL_PARTS'][1].replace('grayscale_', '')
#        image = parent.restrictedTraverse(path)
#        data = image.data
#        event.request.traverse('/Inteligo/' + path)
#        event.request.retry = True
#        event.request.response.setBody(utils.image_to_grayscale(data, path))
##        if IATImage.providedBy(parent):
##            utils.image_to_grayscale(image_body, path)
#    else:
#        pass
        

def GrayscaleTransformations(event):
    """
    Changing the response body by converting
    the images to grayscale and changing the
    css colors definitions to colors from gray
    shades palette
    """
    request = event.request
    context = request.get('PUBLISHED')
    response = event.request.response
    resp_body = response.getBody()
    
    if hasattr(context, 'im_self'):
        context = context.im_self
        
    if hasattr(context, 'context'):
        context = context.context
    
    content_type = ''
    path = ''
    
    if PLONE_RESOURCE_INSTALLED and isinstance (context, FilesystemFile):
        resp_body = context().read()
        path = context.path
        content_type = context.getContentType().split(';')[0]
    
    if isinstance (context, FSImage) or \
       IOFSImage.providedBy(context) or \
       IATImage.providedBy(context) or \
       content_type in ['image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
        if not path:
            path = '/'.join(context.getPhysicalPath())
        image_body = resp_body
        if not image_body and hasattr(context, 'data'):
            image_body = context.data
        if image_body:
            resp_body = utils.image_to_grayscale(image_body, path)
        
    elif IBrowserView.providedBy(request.get('PUBLISHED')) or \
         content_type in ['text/html', 'text/css'] or \
         isinstance(context, (File, FSFile, ATFile, FSPageTemplate)) and \
         context.content_type.split(';')[0] in ['text/html', 'text/css']:
        
        if hasattr(aq_base(context), 'data'):
            resp_body = context.data
            if hasattr(resp_body, 'data'):
                resp_body = resp_body.data
                
        resp_body = utils.add_bodyclass(resp_body)
        resp_body = utils.transform_style_properties(resp_body)
        
    response.setBody(resp_body)
    
