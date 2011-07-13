from django.conf import settings
from django.template import RequestContext
from maintenancemode.http import Http503
from maintenancemode.shortcuts import render_to_503
from maintenancemode.conf.settings import MAINTENANCE_MODE

class MaintenanceModeMiddleware(object):
    def process_request(self, request):
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