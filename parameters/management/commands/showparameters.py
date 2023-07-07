from django.core.management.base import BaseCommand

from parameters.models import Parameter


class Command(BaseCommand):
    help = "Show application parameters"  # noqa: A003"

    def add_arguments(self, parser):
        parser.add_argument(
            "--name",
            dest="parameter_name",
            help="Show this parameter only.",
        )

    def handle(self, *args, **options):
        param_name = options["parameter_name"]

        # Ensure all parameters exist
        Parameter.create_all_parameters()

        if param_name:
            try:
                param = Parameter.objects.get(name=param_name)
                self.stdout.write(f"{param.name}={param.value}")
            except Parameter.DoesNotExist:
                self.stderr.write(f"Parameter {param_name} does not exist!")
        else:
            for param in Parameter.objects.all():
                self.stdout.write(f"{param.name}={param.value}")
