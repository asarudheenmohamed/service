
class CreateListMixin(object):
    """Allows bulk creation of a resource."""
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super(CreateListMixin, self).get_serializer(*args, **kwargs)