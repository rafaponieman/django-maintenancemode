from django.conf import settings
from django.template import RequestContext
from maintenancemode.http import Http503
from maintenancemode.shortcuts import render_to_503
from maintenancemode.conf.settings import MAINTENANCE_MODE
import re

HAS_LANG_PREFIX_RE = re.compile(r"^/(%s)/.*" % "|".join(map(lambda l: re.escape(l[0]), settings.LANGUAGES)))

def has_lang_prefix(path):
    check = HAS_LANG_PREFIX_RE.match(path)
    if check is not None:
        return check.group(1)
    else:
        return False

class MaintenanceModeMiddleware(object):
    def process_request(self, request):
        prefix = has_lang_prefix(request.path_info)
        if prefix:
            path_info = "/" + "/".join(request.path_info.split("/")[2:])
        else:
            path_info = request.path_info
        
        if request.path_info.startswith(settings.MEDIA_URL) \
            or request.path_info.startswith(settings.ADMIN_MEDIA_PREFIX) \
            or path_info.startswith('/admin'): #should be changed to be independent of where the admin is set up
            return None
        
        # Allow access if middleware is not activated
        if not MAINTENANCE_MODE:
            return None
        
        # Allow access if remote ip is in INTERNAL_IPS
        if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return None
        
        # Allow acess if the user doing the request is logged in and a
        # staff member.
        if hasattr(request, 'user') and request.user.is_staff:
            return None
        
        # Otherwise show the user the 503 page
        return self.process_exception(request, Http503())

    def process_exception(self,request,exception):
        if isinstance(exception, Http503):
            return render_to_503(context_instance=RequestContext(request))