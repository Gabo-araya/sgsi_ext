# Celery and Celery beat

Celery can be used to run processing-heavy tasks in background and avoid lengthy request-response cycles.

An example task is defined at `base/tasks.py`.

## Notes when developing tasks.

Task invocation works by constructing a message, **serializing it** and sending it to a message broker.
The broker will distribute the message to the available workers, where the task is actually executed.
Task results are serialized again and sent to the broker where they can be retrieved by your Django app.

Messages are serialized using JSON so beware of custom types:

> The primary disadvantage to JSON is that it limits you to the following data types:
> strings, Unicode, floats, boolean, dictionaries, and lists. Decimals and dates are notably missing.

This also excludes most model instances. Use their PKs instead.

## Testing with a real broker

By default, your dev container will not have Redis and Celery worker available. This is done on purpose to avoid making false assumptions of the final production environment.
Remember that Celery runs on a separate process and can easily scale to multiple nodes if the load demands it, and debugging distributed systems can be hard.
So, when no message broker is defined, Celery enters on a "eager" mode, meaning all tasks are run in the same process as your Django app, synchronously. This eases debugging and testing.

If you absolutely need to test with a proper broker and worker:

1. Remove your `docker-compose.override.yml` and replace it with a proper copy of `docker-compose.dev.yml`
2. Uncomment the celery and redis definitions
2. Edit your .env and define the following variables:
  * `CELERY_BROKER_URL=redis://localhost:6379/1`
  * `CELERY_RESULT_BACKEND=redis://localhost:6379/2`
3. Outside the container, run `docker compose build`.
4. Start the worker process using `docker compose up -d celery`.

The celery worker has no hot reloading support so any change will require a service restart.

## Celery beat

Celery provides a task scheduler that allows us to completely replace django-cron to run periodic tasks.

Tasks are defined in project settings at `CELERY_BEAT_SCHEDULE`. The settings module includes some example tasks and schedules. Multiple schedules are supported:

- Time of day
- Timedeltas (every X seconds/minutes/hours/...)
- Solar events (noon, sunset, dawn, etc.)
- Custom scheduler classes.

This template is configured to store the DB as the schedule. This allows for modification of the existing schedules if required without needing a redeployment.
Please note that tasks are identified by their key, so they won't be updated if changes are made to the settings file.
