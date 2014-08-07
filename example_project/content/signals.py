def sync_post(sender, instance, created, **kwargs):
    from .models import Post  # avoid circular import
    if instance.type != 'post':
        # we only care about posts
        return
    defaults = dict(
        headline=instance.title,
        slug=instance.slug,
        author=unicode(instance.author),  # not python3 compatible
        pub_status='P',  # FIXME
        pub_date=instance.date,
        text=instance.content,
        summary=instance.excerpt,
        wppost=instance,
    )
    if created:
        Post.objects.create(**defaults)
    else:
        post = Post.objects.get(wppost=instance)
        post.__dict__.update(defaults)
        post.save()
