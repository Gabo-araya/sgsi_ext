#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys
import traceback

try:
    import dotenv

    HAVE_DOTENV = True
except ImportError:
    HAVE_DOTENV = False


def main():
    """Run administrative tasks."""
    if HAVE_DOTENV:
        dotenv.load_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print_TODOs_on_runserver()
    execute_from_command_line(sys.argv)


def print_TODOs_on_runserver():
    try:
        from project.settings import DEBUG

        if DEBUG and is_first_runserver():
            common_args = (
                "rg",
                "--word-regexp",
                "--pretty",
            )
            pattern = "T" + "ODO|FIXM" + "E"  # Prevent searching itself
            subprocess.run((*common_args, "--ignore-file=project/.todoignore", pattern))
            subprocess.run((*common_args, "--glob=*.env*", pattern))
            # Run twice because of unoverridable precedences  https://github.com/BurntSushi/ripgrep/issues/1734#issuecomment-730769439
    except Exception:
        # Continue instead of breaking manage.py
        print(traceback.format_exc())


def is_first_runserver():
    try:
        subcommand = sys.argv[1]
    except IndexError:
        subcommand = None

    # runserver calls this every time it reloads, so print on first invocation only:

    def is_runserver_reloader():
        from django.utils.autoreload import DJANGO_AUTORELOAD_ENV

        return os.environ.get(DJANGO_AUTORELOAD_ENV) == "true"

    def is_runserver_plus_reloader():
        from werkzeug.serving import is_running_from_reloader

        return is_running_from_reloader()

    return (subcommand == "runserver" and not is_runserver_reloader()) or (
        subcommand == "runserver_plus" and not is_runserver_plus_reloader()
    )


if __name__ == "__main__":
    main()
