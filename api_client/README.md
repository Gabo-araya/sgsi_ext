# DPT's API Client

DPT's APIClient aims to standardize the way projects connect with external webservices
by providing a common interface to make requests.

## Objectives

- Avoid reinventing the wheel on every project.
- Allow to make both blocking and non-blocking requests, with non-blocking ones being
  the default choice.
- Enforce mandatory error handling.
- Have a log of every request and response received as evidence in case of problems.

The APIClient is built on top of the `requests` library due to its simplicity and
flexibility.

## Classes

### APIClient

This is the base class for the API client. It provides the basic HTTP methods in both
blocking and non-blocking implementation. This class requires to be initialized with
an `APIClientConfiguration` object.

#### Request arguments

GET and DELETE requests consume the following arguments:

* `endpoint`: A string with the API endpoint (without the API prefix)
* `path_params`: In case your endpoint is parameterized, your substitutions are declared
  here.
* `headers`: In case the web service requires special headers, they can be added here.
  Accepts a dictionary of headers and values which are appended to the request.

GET, POST, PUT and PATCH also support:

* `query_params`: Dictionary with query parameters, which are escaped during the request
  process.

POST, PUT, PATCH accept the following arguments:

* `data`: A key-value mapping with data to be sent as urlencoded data.
* `json`: A mapping or array that will be sent as encoded JSON.
* `files`: A mapping of filenames and files.

#### Blocking methods

Blocking methods are recommended for the following use cases:

* When the external response is necessary to deliver a response to the user (like a
  search).
* When the external service is being invoked from a Celery task or a management command.

All blocking methods are appended with the `_blocking` suffix. As the name says, those
methods wait until the remote endpoint delivers its response to the client.

##### Response value for blocking methods

For blocking methods, all response consist on a `(response, error)` tuple. The first
value contains a `requests.Response` object that can be parsed while `error` contains an
error instance containing the reason of the failure.
This response format was deliberately chosen to ease code reviews and ensure errors are
always handled properly.

#### Non-blocking methods

For actions where response times are critical but not its results, non-blocking methods
are the recommended approach. Unlike blocking requests, non-blocking ones are handled
outside the Django's request-response lifecycle, using a Celery job. Typical use cases
for non-blocking requests are sending SMS messages using third-party platforms, or
notify external webservices of an event that happened in our app.

What non-blocking calls basically do is:

1. Check if callbacks are valid functions.
2. Serialize client configuration into a _JSON-able_ object.
3. Invoke a celery task with request parameters and client configuration.
4. Inside the celery worker, reconstruct the client and send request **using the
   blocking implementation.**
5. After a response is received, invoke the defined callbacks.

##### Non-blocking request parameters

In addition to the blocking parameters and just like JavaScript, you must also define
the following arguments:

* `on_success`: Function that will be called in case of a successful response.
* `on_error`: Function that will be called in case of an error.

Both callbacks must be global scope functions. Lambdas and class methods are not valid
as response handlers as they cannot be serialized and because class instances cannot be
sent reliably over a message queue.

### JsonApiClient

Built on top of APIClient, this client allows to interact with webservices that output
JSON, delivering parsed responses.

### APIClientConfiguration

All clients configuration is performed through this class. This is a dataclass that
holds basic settings for each client:

* `code`: a unique code that identifies each client. This code must be one of the values
  defined in `ClientCodes`.
* `host`: hostname and API prefix of the service.
* `scheme`: request scheme to use. It can be either `http` or `https`.
* `timeout`: request timeout in seconds.
* `auth`: authentication class instance. Takes a request and inserts the appropriate
  authentication headers. This setting is optional.

#### Authentication classes

To ensure requests can be executed in non-blocking modes, outside the main worker,
the API client configuration needs to only store JSON-serializable values.
Although almost all settings are basic strings or integers or have a trivial string
representation, the authentication class is typically not.
To remedy this situation, authentication is not transmitted to the worker but
reconstructed entirely when non-blocking calls are used. This was achieved by extending
`requests.AuthBase` to allow the serialization of its initialization parameters and
recreating the instance from serialized data.

##### SerializableAuthBase

This class provides the necessary serialization/deserialization routines to transport
authentication data between nodes. Custom authentication classes must inherit from this
base class and define the `get_init_kwargs()` method to return the required parameters
to properly initialize the class on the non-blocking worker.

### Implementing a custom client

Unless there's a good reason, custom clients should inherit from `APIClient`, as it will
give you blocking and non-blocking support at once. Since non-blocking calls basically
end up calling `request_blocking()` on a separate worker, you only need to override
the blocking implementation, unless your function signature or typing changes.

## Logging

External services cannot be debugged as our apps in case of problems. However, having
request-response logs gives Magnet a way to prove issues do not originate in our
implementation but theirs.

Logs are stored on a separate database. On normal deployments this database will have
the same name as the main one, with a `-logs` suffix. Each time a request is made using
the client, it will be logged here, and as soon as a response is received, the log entry
is updated. Logs can be monitored in the admin site.

### Log pruning

By default, logs of the last 365 days are kept, with routine cleaning performed daily.
The maximum age of logs to keep can be configured via the `API_CLIENT_LOG_MAX_AGE_DAYS`
environment variable.

## Limitations

### Limitations in non-blocking requests

#### File support

As non-blocking requests are processed in a different worker and potentially on a
different host, file support is not currently available.
