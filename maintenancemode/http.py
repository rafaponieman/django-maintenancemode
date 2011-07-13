from django.http import HttpResponse

class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503

    def __init__(self, *args, **kwargs):
        HttpResponse.__init__(self, *args, **kwargs)

class Http503(Exception):
    pass
