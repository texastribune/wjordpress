import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from . import models
from .api import UserCannotReadException


logger = logging.getLogger(__name__)


class HookPressEndpoint(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(HookPressEndpoint, self).dispatch(*args, **kwargs)

    def post(self, request, pk, **kwargs):
        hook_used = request.POST.get('hook')
        site = models.WPSite.objects.get(pk=pk)
        logger.info(u'Hook Triggered: {}'.format(hook_used), extra={
            'request': request,
        })
        # TODO clean up request.POST body so it's more useful
        models.WPLog.objects.push(site, 'hook', request.POST)
        if hook_used == 'save_post':
            try:
                post = models.WPPost.objects.get(
                    wp=site,
                    id=request.POST.get('ID'),
                )
            except models.WPPost.DoesNotExist:
                # need to create
                post = models.WPPost(wp=site, id=request.POST.get('ID'))
            try:
                post.fetch()
            except UserCannotReadException as e:
                # downgrade exception to INFO
                logger.info(e)
        return HttpResponse('OK')
