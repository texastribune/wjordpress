WordPress Quirks
================


Revisions
`````````

What happens when you update a post?

Let's say you have a post (ID=1). When you update it, it's saved and a copy of
the post is created at the next available id (ID=2). So if you check the
``posts/1`` json, you'll see::

    {
        ID: 1,
        status: "publish",
        type: "post",
        ...
    }

And if you check the json for the revision, ``posts/2``, it looks like::

    {
        ID: 2,
        status: "inherit",
        type: "revision",
        ...
    }

If you're using the save hook WordPress plugin, HookPress, you'll get two
pings, one for the original post and one for the revision. If you look at the
Django models, you'll find the post with ID=1 (``original =
WPPost.objects.get(id=1)``) and the revision post (``revision =
WPPost.objects.get(id=2)``) and the revision will be linked to the original
(``revision.parent == original``). So the original ID is retained as the post
is updated.

When you revert to a revision...
