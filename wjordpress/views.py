from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed

from . import models


@csrf_exempt
def hookpress_endpoint(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    hook_used = request.POST.get('hook')
    # TODO log this
    if hook_used == 'save_post':
        # find site
        # TODO don't care about http(s)
        # TODO don't care about trailing slashes
        url, wp_id = request.POST.get('guid').rsplit('?p=', 2)
        site = models.WPSite.objects.get(url=url)
        try:
            post = models.WPPost.objects.get(
                wp=site,
                id=request.POST.get('ID'),
            )
        except models.WPPost.DoesNotExist:
            # need to create
            post = models.WPPost(wp=site, id=request.POST.get('ID'))
        post.fetch()
    return HttpResponse('OK')
