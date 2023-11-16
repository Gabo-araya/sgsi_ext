from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from parameters.models import Parameter


class Command(BaseCommand):
    help = "Set an application parameter."  # noqa: A003"

    def add_arguments(self, parser):
        parser.add_argument(
            "parameter_name",
            help="Parameter name.",
        )
        parser.add_argument(
            "value",
            help="Parameter value.",
        )

    def handle(self, *args, **options):
        param_name = options["parameter_name"]
        param_value = options["value"]

        # Ensure all parameters exist
        Parameter.create_all_parameters()

        try:
            parameter = Parameter.objects.get(name=param_name)
            parameter.value = param_value
            parameter.full_clean()
            parameter.save()
            self.stdout.write("Parameter changed successfully!")
        except Parameter.DoesNotExist:
            self.stderr.write(f"Parameter {param_name} does not exist!")
        except ValidationError as e:
            self.stderr.write(f"Incorrect value for parameter: {e!s}")
