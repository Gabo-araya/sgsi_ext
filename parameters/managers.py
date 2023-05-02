from base.managers import QuerySet


class ParameterQuerySet(QuerySet):
    def search(self, query):
        """
        Search Parameter objects by name
        """
        if query:
            return self.filter(name__unaccent__icontains=query)
        return None
