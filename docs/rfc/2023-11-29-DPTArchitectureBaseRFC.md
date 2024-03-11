# About DPT Architecture - Base

## Context

DPT aims to be a starting point for developing web applications. Therefore, it includes several ready-made models and view classes for common stuff like user management, user-modifiable settings, generic views and so on. Documentation was generally ignored in favor of clean, understandable code.

## Proposed solution

A `base` app will be implemented which will contain a collection of model classes, class-based views and site templates commonly used in Magnet projects.

Generally our models require some kind of audit information in order to determine when it was created or last updated or who did it recently, so all our base models should contain such data in case we need it and a way to update the audit data transparently.

## Modeling

### Models

#### AuditMixin

AuditMixin is a mixin class responsible for creating the respective audit logs in the case of instance creation, edition or deletion. It is mainly invoked from a `post_save` or `post_delete` signal handler.

```plantuml
class base.mixins.AuditMixin {
  _save_log(user, message, action)
  _save_addition(user, message)
  _save_edition(user, message)
  _save_deletion(user)
}
```

#### BaseModel

BaseModel is the DPT way to create models. It combines the base Django's model along with AuditMixin to allow models to log themselves when they are modified, created or deleted.
This class also used to have a JSON serializer for implementing simple JSON views. This feature is deprecated since REST Framework was introduced to DPT, and it is only kept for backwards compatibility.

```plantuml
class django.db.models.Model {}

class base.mixins.AuditMixin {
  _save_log(user, message, action)
  _save_addition(user, message)
  _save_edition(user, message)
  _save_deletion(user)
}
class base.models.BaseModel {
  created_at: DateTimeField
  updated_at: DateTimeField
  __init__(*args, **kwargs)
  update(skip_save, **kwargs)
  to_dict(fields, exclude, include_m2m)
  to_json(fields, exclude, **kwargs)
  get_full_url()
}

base.mixins.AuditMixin <|-- base.models.BaseModel
django.db.models.Model <|- base.models.BaseModel
```

### Model fields

#### BaseFileField

To provide a ready-made way to store user-provided files without the chance of conflicts, `BaseFileField` was developed. This descendant of `BaseField` automatically provides `FileField` with a function to generate unique paths for uploaded files following the schema:

```<model_class>/<year>/<month>/<day>/<uuid>/filename.ext```

### Forms

DPT uses Bootstrap as the design framework. Forms require special treatment to be Bootstrap compatible.

#### BaseFormMixin

This mixin class provides the necessary behaviors to render correctly when used with Bootstrap. It adds the necessary classes depending on the fields being used.

```plantuml
class base.forms.BaseFormMixin {
  __init__(*args, **kwargs)
  hide_field(field_name)
}
```

#### BaseForm and BaseModelForm

`BaseForm` and `BaseModelForm` are the Bootstrap-ready variants of Form and ModelForm, respectively

```plantuml
left to right direction

class base.forms.BaseFormMixin {}
class base.forms.BaseForm {}
class base.forms.BaseModelForm {}

base.forms.BaseFormMixin <|-u- base.forms.BaseForm
django.forms.Form <|-- base.forms.BaseForm
base.forms.BaseFormMixin <|-u- base.forms.BaseModelForm
django.forms.ModelForm <|-- base.forms.BaseModelForm
```

### Views

#### Generic views

DPT should provide extended versions of the built-in generic views of the Django framework. Those views reduce the amount of work necessary to implement simple CRUD views by providing the following behaviors:

* Default authentication checks
* Built-in and customizable permission checking
* Automatically generated titles
* Automatic ordering based on query string params for ListViews
* Cancel and success URLs for create/update/delete views.

Also, additional views were created to support sub-model creation and one-shot model actions: `BaseSubModelCreateView` and `BaseUpdateRedirectView`.

##### List views

BaseListView is an extended ListView with built-in authentication, permission check and user-controlled ordering. Ordering parameters are obtained from the request query string. Each ordering parameter is passed through the `o` key. In a similar way, pagination is controlled via the `p` parameter when the standard `paginate_by` field is set on the implementing class.

```plantuml
skinparam groupInheritance 2

namespace django {
  namespace contrib {
    namespace auth {
      namespace mixins {
        class PermissionRequiredMixin {}
      }
    }
  }
  namespace views {
    namespace generic {
      class ListView {}
    }
  }
}

namespace base.views {
  namespace mixins {
    class LoginPermissionRequiredMixin {
        login_required: bool
        is_login_required()
        dispatch(request, *args, **kwargs)
    }
  }

  namespace generic {
    namespace detail {
      class BaseListView {
        get_title()
        get_context_data(**kwargs)
        get_ordering()
        get_queryset()
      }
    }
  }
}


django.contrib.auth.mixins.PermissionRequiredMixin <|-- base.views.mixins.LoginPermissionRequiredMixin

base.views.mixins.LoginPermissionRequiredMixin <|-- base.views.generic.detail.BaseListView
django.views.generic.ListView <|-- base.views.generic.detail.BaseListView
```

##### Edit views

These views provide the behaviors described ay the beginning of this section. All of them provide the same Django behavior with no changes.

`BaseSubModelCreateView` is a variant of `CreateView` meant to create models that relate closely to a parent one. Examples of such models are:

* Series of an **investment fund**.
* Departments of a **company**.
* Contact addresses of a **user**.

This class works by receiving a request for the parent model and then instantiating a ModelForm for a model with the parent link field already filled such that it can be saved to the database without causing a FK violation while not exposing the field to the user.

The foreign key field can be manually specified using the `model_parent_fk_field`. When not specified, the class tries to infer the field by searching the model for a field that relates to the parent model.

In template, the parent object can be accessed through the `parent_object` or the `<model_name>` context variables.

```plantuml
skinparam groupInheritance 2

namespace django {
  namespace contrib {
    namespace auth {
      namespace mixins {
        class PermissionRequiredMixin {}
      }
    }
  }
  namespace views {
    namespace generic {
      namespace detail {
        class SingleObjectMixin {}
        class SingleObjectTemplateResponseMixin {}
      }
      namespace edit {
        class DeletionMixin {}
        class FormMixin {}
      }
      class RedirectView {}
      class BaseDetailView {}
      class CreateView {}
      class UpdateView {}
    }
  }
}

namespace base.views {
  namespace mixins {
    class LoginPermissionRequiredMixin {
        login_required: bool
        is_login_required()
        dispatch(request, *args, **kwargs)
    }
  }

  namespace generic {
    namespace edit {
      class BaseCreateView {
        get_title()
        get_context_data(**kwargs)
        get_cancel_url()
        get_success_url()
       }
      class BaseUpdateView {
        get_title()
        get_context_data(**kwargs)
        get_cancel_url()
        get_success_url()
       }
      class BaseDeleteView {
        get_title()
        get_context_data(**kwargs)
        get_cancel_url()
        get_success_url()
       }
      class BaseSubModelCreateView {
        parent_model: Model
        parent_object
        parent_pk_url_kwarg: str
        model_parent_fk_field: str
        context_parent_object_name: str
        is_generic_relation: bool
        get(request, *args, **kwargs)
        post(request, *args, **kwargs)
        get_parent_object()
        pre_get(request, *args, **kwargs)
        pre_post(request, *args, **kwargs)
        get_initial_object()
        get_model_related_field_name()
        get_context_data(**kwargs)
        get_context_parent_object_name(parent_obj)
        get_cancel_url()
        get_success_url()
        get_title()
      }
    }
  }
}

django.contrib.auth.mixins.PermissionRequiredMixin <|-- base.views.mixins.LoginPermissionRequiredMixin

base.views.mixins.LoginPermissionRequiredMixin <|-u- base.views.generic.edit.BaseCreateView
django.views.generic.CreateView <|-- base.views.generic.edit.BaseCreateView

base.views.mixins.LoginPermissionRequiredMixin <|-u- base.views.generic.edit.BaseUpdateView
django.views.generic.UpdateView <|-- base.views.generic.edit.BaseUpdateView

base.views.mixins.LoginPermissionRequiredMixin  <|-u- base.views.generic.edit.BaseDeleteView
django.views.generic.detail.SingleObjectTemplateResponseMixin  <|-- base.views.generic.edit.BaseDeleteView
django.views.generic.edit.DeletionMixin  <|-- base.views.generic.edit.BaseDeleteView
django.views.generic.edit.FormMixin  <|-- base.views.generic.edit.BaseDeleteView
django.views.generic.BaseDetailView  <|-- base.views.generic.edit.BaseDeleteView

base.views.mixins.LoginPermissionRequiredMixin <|-u- base.views.generic.edit.BaseSubModelCreateView
django.views.generic.CreateView <|-- base.views.generic.edit.BaseSubModelCreateView

base.views.mixins.LoginPermissionRequiredMixin <|-u- base.views.generic.edit.BaseUpdateRedirectView
django.views.generic.detail.SingleObjectMixin <|-- base.views.generic.edit.BaseUpdateRedirectView
django.views.generic.RedirectView <|-- base.views.generic.edit.BaseUpdateRedirectView
```

##### Detail views

BaseDetailView only differs from DetailView in the addition of title and model class metadata to the template context.

```plantuml
skinparam groupInheritance 2

namespace django {
  namespace contrib {
    namespace auth {
      namespace mixins {
        class PermissionRequiredMixin {}
      }
    }
  }
  namespace views {
    namespace generic {
      class DetailView {}
    }
  }
}

namespace base.views {
  namespace mixins {
    class LoginPermissionRequiredMixin {
        login_required: bool
        is_login_required()
        dispatch(request, *args, **kwargs)
    }
  }

  namespace generic {
    namespace detail {
      class BaseDetailView {
        get_title()
        get_context_data(**kwargs)
        get_cancel_url()
        get_success_url()
      }
    }
  }
}


django.contrib.auth.mixins.PermissionRequiredMixin <|-- base.views.mixins.LoginPermissionRequiredMixin

base.views.mixins.LoginPermissionRequiredMixin <|-- base.views.generic.detail.BaseDetailView
django.views.generic.DetailView <|-- base.views.generic.detail.BaseDetailView
```

#### Miscellaneous views

Three views and a mixin are defined: `SuperuserRestrictedMixin`, `HttpRequestPrintView`, `StatusView` and `BaseTemplateView`. `BaseTemplateView` extends Django's view by providing title to the context.

`SuperuserRestrictedMixin` allows to effectively restrict a view to superuser accounts, while hiding its existence to regular or unauthenticated users (à la GitHub private repos). This is used by `HttpRequestPrintView`, a special live debugging view that responds with a JSON serialization of the original `WSGIRequest` object, used mainly for troubleshooting reverse proxy issues.

`StatusView` allows to review selected project settings without having to inspect the instance through a secure channel. It is restricted to staff users only.

```plantuml
skinparam groupInheritance 2

namespace django {
  namespace contrib {
    namespace auth {
      namespace mixins {
        class PermissionRequiredMixin {}
      }
    }
  }
  namespace views {
    namespace generic {
      class View {}
      class TemplateView {}
    }
  }
}

namespace base.views {
  class HttpRequestPrintView {
    hide_with_404: bool
    dispatch(get, *args, **kwargs)
  }
  namespace misc {
    class StatusView {
      get_context_data(**kwargs)
    }
  }
  namespace mixins {
    class SuperuserRestrictedMixin {}
    class LoginPermissionRequiredMixin {
        login_required: bool
        is_login_required()
        dispatch(request, *args, **kwargs)
    }
  }

  namespace generic {
    namespace base {
      class BaseTemplateView {}
    }
  }
}


django.contrib.auth.mixins.PermissionRequiredMixin <|-- base.views.mixins.LoginPermissionRequiredMixin

base.views.mixins.LoginPermissionRequiredMixin <|-- base.views.generic.base.BaseTemplateView
django.views.generic.TemplateView <|-- base.views.generic.base.BaseTemplateView

base.views.generic.base.BaseTemplateView <|-- base.views.misc.StatusView

base.views.mixins.SuperuserRestrictedMixin <|-- base.views.HttpRequestPrintView
django.views.generic.View <|-- base.views.HttpRequestPrintView
```
