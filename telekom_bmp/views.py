import logging

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .events import fetch_event


log = logging.getLogger(__name__)


class Event(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)

    def get(self, request):
        param = request.GET.get('url', 'didnt get any url')
        log.debug("subscription callback, calling %s" % param)
        return HttpResponse(fetch_event(param),
                            content_type="application/xml")
