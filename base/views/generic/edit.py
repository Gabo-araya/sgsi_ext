from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import ForeignKey
from django.db.models import ProtectedError
from django.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic.detail import BaseDetailView as GenericBaseDetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseCreateView as GenericBaseCreateView
from django.views.generic.edit import BaseUpdateView as GenericBaseUpdateView
from django.views.generic.edit import DeletionMixin
from django.views.generic.edit import FormMixin

from ..mixins import LoginPermissionRequiredMixin


class BaseCreateView(LoginPermissionRequiredMixin, CreateView):
    login_required = True
    permission_required = ()
    next_url = None
    title = None

    def get_title(self):
        if self.title is not None:
            return self.title
        verbose_name = self.model._meta.verbose_name
        return _("Create {}").format(verbose_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.next_url = self.request.GET.get("next")

        context["next"] = self.next_url

        context["opts"] = self.model._meta
        context["title"] = self.get_title()
        context["cancel_url"] = self.get_cancel_url()

        return context

    def get_cancel_url(self):
        if self.next_url:
            return self.next_url

        model_name = self.model.__name__.lower()
        return reverse(f"{model_name}_list")

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        if next_url:
            return next_url

        return super().get_success_url()


class BaseSubModelCreateView(LoginPermissionRequiredMixin, CreateView):
    """
    Create view when the object is nested within a parent object
    """

    parent_model = None
    parent_object = None
    parent_pk_url_kwarg = "parent_pk"
    model_parent_fk_field = None
    context_parent_object_name = None
    login_required = True
    permission_required = ()
    is_generic_relation = False
    next_url = None
    title = None

    def get(self, request, *args, **kwargs):
        self.parent_object = self.get_parent_object()
        self.object = self.get_initial_object()
        # Give a chance to declare further instance attributes
        self.pre_get(request, *args, **kwargs)
        return super(GenericBaseCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.parent_object = self.get_parent_object()
        self.object = self.get_initial_object()
        # Give a chance to declare further instance attributes
        self.pre_post(request, *args, **kwargs)
        return super(GenericBaseCreateView, self).post(request, *args, **kwargs)

    def get_parent_object(self):
        parent_pk = self.kwargs.get(self.parent_pk_url_kwarg)
        return get_object_or_404(self.parent_model, pk=parent_pk)

    def pre_get(self, request, *args, **kwargs):
        """
        Allows to perform several operations before the superclass get()
        generates the response.
        """

    def pre_post(self, request, *args, **kwargs):
        """
        Allows to perform several operations before the superclass post()
        generates the response.
        """

    def get_initial_object(self):
        """Gets an object previously initialized with the parent object."""
        parent_pk = self.kwargs.get(self.parent_pk_url_kwarg)
        if self.is_generic_relation:
            parent_content_type = ContentType.objects.get_for_model(self.parent_model)
            obj = self.model(
                object_id=parent_pk,
                content_type=parent_content_type,
            )
        else:
            parent_obj = self.parent_object
            related_field_name = self.get_model_related_field_name()
            obj = self.model(**{related_field_name: parent_obj})

        return obj

    def get_model_related_field_name(self):
        """
        Gets the field name that relates model with its parent model.
        If `model_parent_fk_field` is defined, it uses that value. Otherwise,
        traverse the model declared fields and return the first ForeignKey
        field relating to the parent model.
        """
        if self.model_parent_fk_field is not None:
            return self.model_parent_fk_field

        for field in self.model._meta.get_fields():
            if (
                isinstance(field, ForeignKey)
                and field.related_model == self.parent_model
            ):
                return field.name

        msg = (
            "No model_parent_fk_field declared and no field relating to "
            f"{self.parent_model.__name__} was found in {self.model.__name__,}"
        )
        raise ImproperlyConfigured(msg)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["parent_object"] = self.parent_object
        context_parent_object_name = self.get_context_parent_object_name(
            self.parent_object,
        )
        if context_parent_object_name:
            context[context_parent_object_name] = self.parent_object
        context["title"] = self.get_title()

        self.next_url = self.request.GET.get("next")
        context["next"] = self.next_url
        context["cancel_url"] = self.get_cancel_url()

        return context

    def get_context_parent_object_name(self, parent_obj):
        """Get the name to use for the parent object."""
        if self.context_parent_object_name:
            return self.context_parent_object_name
        if isinstance(parent_obj, models.Model):
            return parent_obj._meta.model_name
        return None

    def get_cancel_url(self):
        if self.next_url:
            return self.next_url

        return self.parent_object.get_absolute_url()

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        if next_url:
            return next_url

        return super().get_success_url()

    def get_title(self):
        if self.title is not None:
            return self.title
        verbose_name = self.model._meta.verbose_name
        return _("Create {}").format(verbose_name)


class BaseUpdateView(LoginPermissionRequiredMixin, UpdateView):
    login_required = True
    permission_required = ()
    next_url = None
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.next_url = self.request.GET.get("next")

        context["next"] = self.next_url

        context["opts"] = self.model._meta
        context["cancel_url"] = self.get_cancel_url()
        context["title"] = self.get_title()

        return context

    def get_title(self):
        if self.title is not None:
            return self.title
        return _("Update {}").format(str(self.object))

    def get_cancel_url(self):
        if self.next_url:
            return self.next_url

        return self.object.get_absolute_url()

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        if next_url:
            return next_url

        return super(GenericBaseUpdateView, self).get_success_url()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.title = self.get_title()
        return super(GenericBaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.title = self.get_title()
        return super(GenericBaseUpdateView, self).post(request, *args, **kwargs)


# NOTE: we could use DeleteView as well, but it may break existing applications.
class BaseDeleteView(
    LoginPermissionRequiredMixin,
    SingleObjectTemplateResponseMixin,
    DeletionMixin,
    FormMixin,
    GenericBaseDetailView,
):
    form_class = Form
    login_required = True
    permission_required = ()
    next_url = None
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.next_url = self.request.GET.get("next")

        context["next"] = self.next_url

        context["opts"] = self.model._meta
        context["title"] = self.get_title()

        return context

    def get_title(self):
        if self.title is not None:
            return self.title
        return _("Delete {}").format(str(self.object))

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        if next_url:
            return next_url

        model_name = self.model.__name__.lower()
        return reverse(f"{model_name}_list")

    def post(self, request, *args, **kwargs):
        # Set self.object before the usual form processing flow.
        # Inlined because having DeletionMixin as the second base, for
        # get_success_url(), makes leveraging super() with ProcessFormView
        # overly complex.
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            return self.handle_protected_error(request, error)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError as error:
            return self.handle_protected_error(self.request, error)

    def handle_protected_error(self, request, error):
        """
        Overwrite this method if you want to change the error message or
        redirect to a different view.
        """
        messages.add_message(
            request,
            messages.ERROR,
            _("This object cannot be deleted."),
        )
        return HttpResponseRedirect(self.object.get_absolute_url())


class BaseUpdateRedirectView(
    LoginPermissionRequiredMixin,
    SingleObjectMixin,
    RedirectView,
):
    login_required = True
    permission_required = ()

    permanent = False

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.do_action()
        return super().post(request, *args, **kwargs)

    def do_action(self):
        """
        Implement this method with the action you want to do before redirect
        """

    def get_redirect_url(self, *args, **kwargs):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url

        return self.object.get_absolute_url()
