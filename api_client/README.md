# DPT's  API Client

DPT's APIClient aims to standardize the way projects connect with external webservices
by providing a common interface to make requests.

## Objectives

- Avoid reinventing the wheel on every project.
- Allow to make both blocking and non-blocking requests, with non-blocking ones being
  the default choice.
- Enforce mandatory error handling.
- Have a log of every request and response received as evidence in case of problems.

## Classes

### APIClient

This is the base class for the API client. It provides the basic HTTP methods in both
blocking and non-blocking implementation.

#### Structure of a request

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

For tasks where there is no need to respond as soon as possible, such as management
commands and Celery tasks, blocking methods can be used. All blocking methods are
appended with the `_blocking` suffix. As the name says, those methods wait until the
remote endpoint delivers its response to the client.

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

### Implementing a custom client

TODO

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
