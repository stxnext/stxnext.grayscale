from OFS.Image import File
from Products.CMFCore.FSFile import FSFile
from Products.CMFCore.FSImage import FSImage
from plone.app.linkintegrity.interfaces import IOFSImage
from zope.publisher.interfaces.browser import IBrowserView

import utils

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
    
    if isinstance (context, FSImage) or IOFSImage.providedBy(context):
        path = '/'.join(context.getPhysicalPath())
        resp_body = utils.image_to_grayscale(resp_body, path)
        
    elif IBrowserView.providedBy(request.get('PUBLISHED')) or \
         isinstance(context, (File, FSFile)) and \
         context.content_type.split(';')[0] in ['text/css', 'text/html']:
        
        matches = utils.COLOR_PATTERN.findall(resp_body)
        for match in set(matches):
            r, g, b = utils.htmls_color_to_rgb(match)
            average = (r + g + b) / 3
            gray_color = utils.rgb_to_html_color((average, average, average))
            resp_body = resp_body.replace(match, gray_color)
            
    response.setBody(resp_body)
    