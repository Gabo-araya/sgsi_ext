# Reference

## Models

### BaseModel

Every model has to inherit from the class BaseModel. This allows that every model has the fields `created_at` and `updated_at` and methods like `to_json` and `to_dict`.

#### update

This is a shortcut method, it basically sets all keyword arguments as attributes on the calling object, then it stores only those values into the database.

To store values into the database, this method uses the `save` method with the `update_fields` parameter, but if you want to skip the save method, you can pass the parameter `skip_save=True` when calling update (useful when you want to avoid calling save signals).

### OrderableModel

This model inherits from BaseModel. It adds the `display_order` field to allow customizable ordering. Change the `set_display_order_` method to change the logic of how a new object is arranged.

## Forms

### BaseModelForm

Every Form has to inherit from this class because it allows a correct integration with
bootstrap and JS components. For example, date fields will contain a class that is
picked up by the datepicker javascript library and render a datepicker input.

If you are handling Chilean RUTs, you can install [Django Local Flavor](https://github.com/django/django-localflavor).

## Views

Contains classes that inherit from Django generic class based views. This is done to add new features to these classes.

### LoginPermissionRequiredMixin

This class inhertis from django's AccessMixin. Verifies that the current user is authenticated (if the attribute login_required is True) and has the required permission (if permission_required is set).

### Classes

#### BaseTemplateView

Renders a given template. Inherits from [TemplateView](https://docs.djangoproject.com/en/4.2/ref/class-based-views/base/#templateview).

#### BaseDetailView

Renders a given object. Inherits from [DetailView](https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-display/#detailview).

#### BaseListView

Renders a list of objects. Inherits from [ListView](https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-display/#listview).

#### BaseCreateView

Renders a form to create a single object for a given model. Inherits from [CreateView](https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#createview).

#### BaseUpdateView

Renders a form to update a single object of a given model. Inherits from  [UpdateView](https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#updateview).

#### BaseDeleteView

Renders a form to delete a single object of a given model. Inherits from [DeleteView](https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#deleteview).

#### BaseRedirectView

Redirects to a given url. Inherits from [RedirectView](https://docs.djangoproject.com/en/4.2/ref/class-based-views/base/#redirectview).

#### BaseUpdateRedirectView

Redirects to a given url after calling the method `do_action`. Useful when processing something and then redirecting to show the result. Inherits from BaseRedirectView

#### StatusView

View that shows internal data of the site, for example if the CAPTCHA is activated or if the site has google analytics.

#### FormsetCreateView

View to create an object and a list of child objects with a form and a [formset](https://docs.djangoproject.com/en/4.2/topics/forms/formsets/).

#### FormsetUpdateView

View to update an object and a list of child objects with a form and a [formset](https://docs.djangoproject.com/en/4.2/topics/forms/formsets/).

## Custom apps

### Regions

App with the list for regions and communes of Chile. Both models are populated by migrations.

### Parameters

App to set application wide parameters in the admin.

The parameters are stored in the `Parameter` model and can be retrieved with `Parameter.value_for(param_name)`. Using this method is recommended since it uses CACHE (since it is assumed that parameters rarely change).

To set a list Parameters that the app needs with their default values, place them in `parameters/definitions.py`. There is an example with a parameter called `DEFAULT_URL_PROTOCOL`.

### Users

App that overrides the Django User with the class `User` that is easily modifiable.

## Base template: base.html

All view templates should extend base.html, this renders the layout with a navbar and the footer. This templates has the following blocks:

1. title: Set the content of the title meta tag. By default, is set to the `title` variable.
2. stylesheets: A place to put stylesheets for the given template. By default, is empty. Be careful to use this block, it should only be used when the vite-compiled styles are not enough for some reason.
3. breadcrumbs: A place to put breadcrumb elements after the `home` element and before the element that contains the `title`.
4. content_title: The place to put the `h1` tag. By default, contains a `h1` tag with the `title` and a place to put buttons
5. options: A place to put buttons beside the `h1` tag.
6. content: The main content of the page. **This should always be defined in the template**
7. legacy_javascripts: A place to put javascripts for the given template. By default, is empty. Be careful to use this block, it should only be used when the vite-compiled javascripts are not enough for some reason.

All these blocks are optional **except content** since they have default implementations.

The included navbar template can be found in `base/templates/includes/navbar.html`.
The included footer template can be found in `base/templates/includes/footer.html`.

## API Client

DPT includes an API client app to standardize the development of external integrations. An example integration is available in the `dummy_app` directory.

For additional documentation, see the `api_client/README.md` file.
