from base.managers import BaseQuerySet


class ParameterQuerySet(BaseQuerySet):
    def search(self, query):
        """
        Search Parameter objects by name
        """
        if query:
            return self.filter(name__unaccent__icontains=query)
        return None
