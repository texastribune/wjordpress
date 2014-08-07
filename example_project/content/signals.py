def post_to_post(wppost, created):
    from .models import Post  # avoid circular import
    defaults = dict(
        headline=wppost.title,
        slug=wppost.slug,
        author=unicode(wppost.author),  # not python3 compatible
        pub_status='P',  # FIXME
        pub_date=wppost.date,
        text=wppost.content,
        summary=wppost.excerpt,
        wppost=wppost,
    )
    if created:
        Post.objects.create(**defaults)
    else:
        post = Post.objects.get(wppost=wppost)
        post.__dict__.update(defaults)
        post.save()


def post_to_image(wppost, created):
    from .models import RemoteImage  # avoid circular import
    defaults = dict(
        src=wppost.attachment_meta['sizes'].values()[0]['url'],
    )
    if created:
        RemoteImage.objects.create(**defaults)
    else:
        image = RemoteImage.objects.get(wppost=wppost)
        image.__dict__.update(defaults)
        image.save()


def sync_post(sender, instance, created, **kwargs):
    if instance.type == 'post':
        post_to_post(instance, created)
    elif instance.type == 'attachment':
        post_to_image(instance, created)
