from .generic import BaseCreateView
from .generic import BaseUpdateView


class FormsetViewMixin:
    formset_class = None
    initial_formset = {}
    prefix_formset = None

    def get_formset_class(self):
        return self.formset_class

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = self.get_formset()
        form = self.get_form()
        return self.render_to_response(
            self.get_context_data(formset=formset, form=form),
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form_valid = super().form_valid(form)
        formset.instance = self.object
        formset.save()
        return form_valid

    def get_initial_formset(self):
        """Return the initial data to use for formset on this view."""
        return self.initial_formset.copy()

    def get_prefix_formset(self):
        """Return the prefix to use for formset."""
        return self.prefix_formset

    def get_formset_kwargs(self):
        kwargs = {
            "initial": self.get_initial_formset(),
            "prefix": self.get_prefix_formset(),
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                },
            )
        return kwargs

    def get_formset(self, formset_class=None):
        """Return an instance of the form to be used in this view."""
        if formset_class is None:
            formset_class = self.get_formset_class()
        return formset_class(**self.get_formset_kwargs())

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset),
        )


class FormsetCreateView(FormsetViewMixin, BaseCreateView):
    def get_object(self, queryset=None):
        return None


class FormsetUpdateView(FormsetViewMixin, BaseUpdateView):
    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating formset."""
        kwargs = super().get_formset_kwargs()
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs
