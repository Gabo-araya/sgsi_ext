from __future__ import annotations

# standard library
import operator

from argparse import RawTextHelpFormatter
from collections.abc import Iterable
from functools import reduce
from pathlib import Path
from typing import TYPE_CHECKING

# django
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db.models import Q

import yaml

from users.models.group import Group

if TYPE_CHECKING:
    from django.db.models import QuerySet

MANAGE_PREFIX = "manage_"
MANAGE_ALL_SHORTCUT = "manage_all"
VIEW_ALL_SHORTCUT = "view_all"
PERMISSION_SEPARATOR = "."


class Command(BaseCommand):
    help = """
    Creates groups with the specified permissions according to the schema defined in
    group_schema.yaml.

    The schema format should be:

    - GroupName:
        - Permission
        - Permission

    - GroupName: []

    where:
    - GroupName is the name of the group.
    - Permission is the permision in the <app>.<codename> format.
    - [] is an empty list.

    There are some shortcut codenames which are:
    - manage_<model>: Translates into all the permissions for the given model.
    - manage_all: Will add all the permissions of a given app.
    - view_all: Will add all the view permissions of a given app.
    """  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument(
            "--sync",
            action="store_true",
            default=False,
            help=(
                "Sync mode will sync the permission schema even if it means deleting "
                "user defined groups or remove permissions."
            ),
        )

    def handle(self, sync, *args, **options):
        schema_path = Path("users/management/group_schema.yaml")
        schema = self.get_group_schema(schema_path)
        schema = self.clean_schema(schema)
        msg = "Syncing groups..." if sync else "Updating groups..."
        self.print_to_stdout(msg, True)
        self.update_groups(schema, sync=sync)

    def get_group_schema(self, schema_path: Path) -> dict[str, Iterable[str]]:
        """
        Parses the YAML file and returns a Dict.
        """
        if not schema_path.is_file():
            msg = "Path is not a file or does not exist."
            raise CommandError(msg)
        with schema_path.open() as file:
            try:
                schema = yaml.safe_load(file)
            except yaml.scanner.ScannerError as exc:
                msg = "File is not YAML loadable."
                raise CommandError(msg) from exc
        return schema

    def clean_schema(self, schema: dict[str, Iterable[str]]) -> dict[str, set[str]]:
        """
        Validates and cleans the schema.
        """
        self.validate_schema_format(schema)
        new_schema = self.transform_schema(schema)
        self.validate_schema_permissions(new_schema)
        return new_schema

    def validate_schema_format(self, schema: dict[str, Iterable[str]]) -> None:
        """
        Validates that the dict format is {GroupName: [Permission]} where GroupName is a
        string and Permission is a string with the format <app>.<codename>'.
        """
        base_msg = "Wrong schema format: "
        for group_name, perms in schema.items():
            if not isinstance(group_name, str):
                msg = base_msg + "All groups must be string."
                raise CommandError(msg)
            for perm in perms:
                if not isinstance(perm, str):
                    msg = base_msg + "All permissions must be string."
                    raise CommandError(msg)
                if perm.count(PERMISSION_SEPARATOR) != 1:
                    msg = base_msg + "Permissions format should be app.codename."
                    raise CommandError(msg)

    def transform_schema(self, schema: dict[str, Iterable[str]]) -> dict[str, set[str]]:
        """
        Transforms codenames shortcuts to the corresponding permissions.
        """
        new_schema = {}
        for group, permissions in schema.items():
            new_permissions = set()
            for permission in permissions:
                app, codename = permission.split(PERMISSION_SEPARATOR)
                if codename == MANAGE_ALL_SHORTCUT:
                    queryset = Permission.objects.filter(
                        content_type__app_label=app,
                    )
                elif codename == VIEW_ALL_SHORTCUT:
                    queryset = Permission.objects.filter(
                        codename__startswith="view_",
                        content_type__app_label=app,
                    )
                elif codename.startswith(MANAGE_PREFIX):
                    model_name = codename.replace(MANAGE_PREFIX, "")
                    queryset = Permission.objects.filter(
                        content_type__app_label=app,
                        content_type__model=model_name,
                    )
                else:
                    new_permissions.add(permission)
                    continue
                if not queryset.exists():
                    msg = (
                        f'Cannot find any permissions for app "{app}" and codename '
                        f'"{codename}"'
                    )
                    raise CommandError(msg)
                new_permissions.update(self.get_permission_strings(queryset))
            new_schema[group] = new_permissions
        return new_schema

    def validate_schema_permissions(self, schema: dict[str, set[str]]):
        """
        Validates that all permissions in schema exist in the database.

        If a permission doesnt exist it raises a CommandError.
        """
        schema_perms = reduce(operator.or_, schema.values(), set())
        lookup_expr = self.get_lookup_expression(schema_perms)
        queryset = Permission.objects.filter(lookup_expr)
        retrieved_perms = self.get_permission_strings(queryset)
        excess_permissions = schema_perms - retrieved_perms
        if excess_permissions:
            perms_str = ", ".join(excess_permissions)
            msg = (
                f"The following permissions don't exist in the database: [{perms_str}]."
            )
            raise CommandError(msg)

    def get_lookup_expression(self, perms: set[str]) -> Q:
        """
        perms is an set of strings where each string should have the format
        app.codename.

        Returns a lookup expression of combined Q objects with the OR SQL operator.
        """
        if not perms:
            return Q(pk=None)
        lookups = (
            Q(content_type__app_label=app, codename=codename)
            for app, codename in (perm.split(PERMISSION_SEPARATOR) for perm in perms)
        )
        return reduce(operator.or_, lookups)

    def get_permission_strings(
        self, queryset: QuerySet[Permission] | None = None
    ) -> set[str]:
        """
        Takes a Permission queryset and returns a set of string with the format
        app.codename.
        """
        if queryset is None:
            queryset = Permission.objects.all()
        values_list = queryset.values_list("content_type__app_label", "codename")
        return {".".join(perm_tuple) for perm_tuple in values_list}

    def update_groups(self, schema: dict[str, set[str]], sync: bool = False) -> None:
        """
        It updates the groups and permissions according to schema.
        If a group doesnt exist it will create it.
        If a group exists it will update the permissions.

        If sync mode is enabled it will delete existing groups that
        are not in schema.
        """
        if sync:
            self.delete_groups(schema)

        default_perm_codenames = schema.get(settings.DEFAULT_GROUP_NAME, set())
        for group_name, perm_codenames in schema.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.print_to_stdout(f"Created group {group_name}.", True)
            else:
                self.print_to_stdout(f"Group {group_name} exists.", True)

            if group_name != settings.DEFAULT_GROUP_NAME:
                perm_codenames.update(default_perm_codenames)

            self.update_permissions(group, perm_codenames, sync=sync)
            self.print_to_stdout()

    def delete_groups(self, schema: dict[str, set[str]]) -> None:
        """
        Deletes groups that are not in schema.
        """
        schema_groups = set(schema.keys())
        groups_to_delete = Group.objects.exclude(name__in=schema_groups)
        deleted_groups = tuple(groups_to_delete)
        groups_to_delete.delete()

        for group_name in deleted_groups:
            self.print_to_stdout(f"The group {group_name} was deleted.", True)

    def update_permissions(
        self, group: Group, schema_perms: set[str], sync: bool = False
    ) -> None:
        """
        Creates the permissions specified in schema.

        If sync mode is enabled it will remove permissions that are not
        specified in schema.
        """
        lookup_expr = self.get_lookup_expression(schema_perms)
        permissions = Permission.objects.filter(lookup_expr)

        current_permissions = self.get_permission_strings(group.permissions.all())
        perms_to_set = self.get_permission_strings(permissions)

        if sync:
            group.permissions.set(permissions)
        else:
            group.permissions.add(*permissions)

        self.print_permissions_diff(group, current_permissions, perms_to_set, sync)

    def print_permissions_diff(
        self,
        group: Group,
        current_permissions: set[str],
        perms_to_set: set[str],
        sync: bool,
    ) -> None:
        """
        Prints the permissions that were added and removed.
        """
        added_perms = sorted(perms_to_set - current_permissions)
        self.print_to_stdout(f"{group.name}:")
        if added_perms:
            self.print_to_stdout("\tAdded permissions:")
        else:
            self.print_to_stdout("\tNo permissions added.")
        for perm in added_perms:
            self.print_to_stdout(f"\t\t- {perm}")
        self.print_to_stdout()
        removed_perms = sorted(current_permissions - perms_to_set) if sync else ()
        if removed_perms:
            self.print_to_stdout("\tRemoved permissions:")
        else:
            self.print_to_stdout("\tNo permissions removed.")
        for perm in removed_perms:
            self.print_to_stdout(f"\t\t- {perm}")

    def print_to_stdout(self, message: str = "", add_line_break: bool = False) -> None:
        """
        Helper function to print to stdout.
        """
        self.stdout.write(message)
        if add_line_break:
            self.stdout.write()

    def create_parser(self, *args, **kwargs):
        """
        We change the formatter_class to support line breaks in the help text.
        """
        parser = super().create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser
