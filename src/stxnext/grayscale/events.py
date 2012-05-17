from Acquisition import aq_base
from OFS.Image import File
from Products.CMFCore.FSFile import FSFile
from Products.CMFCore.FSImage import FSImage
from Products.ATContentTypes.interface.image import IATImage
from Products.ATContentTypes.content.file import ATFile
from plone.app.linkintegrity.interfaces import IOFSImage
from zope.app.component.hooks import getSite
from zope.browserresource.file import File as browserresourcefile
from zope.publisher.interfaces.browser import IBrowserView
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.FSPageTemplate import FSPageTemplate
from zExceptions import NotFound

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
    portal = getSite()
    if not portal:
        return
    properties_tool = getToolByName(portal, 'portal_properties')
    transformed_themes = properties_tool.site_properties.getProperty('transformed_themes')
    if not transformed_themes:
        return
    skins_tool = getToolByName(portal, 'portal_skins')
    request_varname = skins_tool.request_varname
    if request.get(request_varname):
        selected_skin = request.get(request_varname)
    else:
        selected_skin = skins_tool.getDefaultSkin()
    if selected_skin in transformed_themes:
        GrayscaleTransformations(event)

def GrayscaleTransformations(event):
    """
    Changing the response body by converting
    the images to grayscale and changing the
    css colors definitions to colors from gray
    shades palette
    """
    request = event.request
    response = request.response
    context = request.get('PUBLISHED')
    resp_body = response.getBody()
    content_type = ''
    path = ''
    if hasattr(context, 'im_self'):
        context = context.im_self
        
    if hasattr(context, 'context'):
        context = context.context
    
    if PLONE_RESOURCE_INSTALLED and isinstance (context, FilesystemFile):
        resp_body = context().read()
        path = context.path
        content_type = context.getContentType().split(';')[0]
    
    try:
        filename = context.getId()
    except AttributeError:
        filename = context.__name__
    except:
        return
    
    images_content_types = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif']
    
    if isinstance (context, FSImage) or \
       IOFSImage.providedBy(context) or \
       IATImage.providedBy(context) or \
       content_type in images_content_types or \
       isinstance (context, browserresourcefile) and \
       context.content_type.split(';')[0] in images_content_types:
        
        if not path:
            try:
                path = '/'.join(context.getPhysicalPath())
            except AttributeError:
                path = filename
                        
        try:
            resp_body = utils.get_resource(request, response, filename)
        except NotFound:
            image_body = resp_body
            if not image_body and hasattr(context, 'data'):
                image_body = context.data
            if image_body:
                resp_body = utils.image_to_grayscale(image_body, path)
            utils.store_resource(filename, resp_body)
        
    elif IBrowserView.providedBy(request.get('PUBLISHED')) or \
         content_type in ['text/html', 'text/css'] or \
         isinstance(context, (File, FSFile, ATFile, FSPageTemplate)) and \
         context.content_type.split(';')[0] in ['text/html', 'text/css']:
        
        if hasattr(aq_base(context), 'data'):
            resp_body = context.data
            if hasattr(resp_body, 'data'):
                resp_body = resp_body.data
        
        if content_type == 'text/css' or \
           isinstance(context, (File, FSFile, ATFile, FSPageTemplate)) and \
           context.content_type.split(';')[0] == 'text/css':
            
            try:
                resp_body = utils.get_resource(request, response, filename)
            except NotFound:                
                resp_body = utils.transform_style_properties(resp_body)
                utils.store_resource(filename, resp_body)
                
        else:
            resp_body = utils.add_bodyclass(resp_body)
            resp_body = utils.transform_style_properties(resp_body)
            
    response.setBody(resp_body)
    
