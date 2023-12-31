"""Helper command to run some post install tasks."""
import argparse

from django.core.management import call_command
from django.core.management.base import BaseCommand


HELP_TEXT = """
Performs Division 2 DB common server upgrade operations using a single entrypoint.
This will run the following management commands with default settings, in order:
- migrate
- collectstatic
- clearsessions

"""


class Command(BaseCommand):
    """Override the BaseCommand class."""

    help = HELP_TEXT

    def create_parser(self, *args, **kwargs):
        """Custom parser that can display multiline help."""
        parser = super().create_parser(*args, **kwargs)
        parser.formatter_class = argparse.RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        """Parse any provided arguments and append them to the command."""
        parser.add_argument(
            "--no-clearsessions",
            action="store_false",
            dest="clearsessions",
            default=True,
            help="Do not automatically clean out expired sessions.",
        )
        parser.add_argument(
            "--no-collectstatic",
            action="store_false",
            dest="collectstatic",
            default=True,
            help="Do not automatically collect static files into a single location.",
        )
        parser.add_argument(
            "--no-migrate",
            action="store_false",
            dest="migrate",
            default=True,
            help="Do not automatically perform any database migrations.",
        )

    def handle(self, *args, **options):
        """Execute the helper methods."""
        # Run migrate
        if options.get("migrate"):
            print("Performing database migrations...")
            call_command(
                "migrate",
                interactive=False,
                traceback=options["traceback"],
                verbosity=options["verbosity"],
            )
            print()

        # Run collectstatic
        if options.get("collectstatic"):
            print("Collecting static files...")
            call_command("collectstatic", interactive=False)
            print()

        # Run clearsessions
        if options.get("clearsessions"):
            print("Removing expired sessions...")
            call_command("clearsessions")
            print()
