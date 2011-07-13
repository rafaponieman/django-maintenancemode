from django.template import Template, loader, TemplateDoesNotExist, Context
from maintenancemode.http import HttpResponseServiceUnavailable

def render_to_503(*args, **kwargs):
    """
        Returns a HttpResponseForbidden whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
    """
    if not isinstance(args,list):
        args = []
        args.append('503.html')

    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    try:
        response = HttpResponseServiceUnavailable(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)
    except TemplateDoesNotExist:
        response = HttpResponseServiceUnavailable(Template('Service Unavailable').render(Context()), **httpresponse_kwargs)

    return response