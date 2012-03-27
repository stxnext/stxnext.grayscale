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

try:
    from plone.resource.file import FilesystemFile
except ImportError:
    pass

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

def GrayscaleTransformations(event):
    """
    Changing the response body by converting
    the images to grayscale and changing the
    css colors definitions to colors from gray
    shades palette
    """
    # TODO:
    # configureable enabled,
    # configureable transformable skin names,
    # transformating other (than hex) conventions of colors definitions
    # rename the images paths to avoid browser cache
    # save the transformed images in ZODB and fallback to them if possible
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
    
    if isinstance (context, FilesystemFile):
        resp_body = context().read()
        path = context.path
        content_type = context.getContentType()
        
    if isinstance (context, FSImage) or \
       IOFSImage.providedBy(context) or \
       IATImage.providedBy(context) or \
       content_type.split(';')[0] in ['image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
        if not path:
            path = '/'.join(context.getPhysicalPath())
        image_body = resp_body
        if not image_body and hasattr(context, 'data'):
            image_body = context.data
        if image_body:
            resp_body = utils.image_to_grayscale(image_body, path)
        
    elif IBrowserView.providedBy(request.get('PUBLISHED')) or \
         content_type.split(';')[0] in ['text/css', 'text/html'] or \
         isinstance(context, (File, FSFile, ATFile)) and \
         context.content_type.split(';')[0] in ['text/css', 'text/html']:
        if hasattr(context, 'data'):
            resp_body = context.data
        matches = utils.COLOR_PATTERN.findall(resp_body)
        for match in set(matches):
            r, g, b = utils.htmls_color_to_rgb(match)
            average = (r + g + b) / 3
            gray_color = utils.rgb_to_html_color((average, average, average))
            resp_body = resp_body.replace(match, gray_color)
        resp_body = utils.add_bodyclass(resp_body)

            
    response.setBody(resp_body)
    
