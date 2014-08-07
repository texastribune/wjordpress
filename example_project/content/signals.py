def post_to_post(wppost, created):
    from .models import Post, RemoteImage  # avoid circular import
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
    if wppost.featured_image:
        try:
            image = RemoteImage.objects.get(wppost=wppost.featured_image)
            defaults['lede_art'] = image
        except RemoteImage.DoesNotExist:
            # next time
            pass
    if created:
        Post.objects.create(**defaults)
    else:
        post = Post.objects.get(wppost=wppost)
        post.__dict__.update(defaults)
        post.save()


def post_to_image(wppost, created):
    from .models import Post, RemoteImage  # avoid circular import
    defaults = dict(
        src=wppost.attachment_meta['sizes'].values()[0]['url'],
        wppost=wppost,
    )
    if created:
        image = RemoteImage.objects.create(**defaults)
    else:
        image = RemoteImage.objects.get(wppost=wppost)
        image.__dict__.update(defaults)
        image.save()
    if wppost.parent:
        # associate lede art
        try:
            post = Post.objects.get(wppost=wppost.parent)
            post.lede_art = image
            post.save()
        except Post.DoesNotExist:
            # next time
            pass


def sync_post(sender, instance, created, **kwargs):
    if instance.type == 'post':
        post_to_post(instance, created)
    elif instance.type == 'attachment':
        post_to_image(instance, created)
