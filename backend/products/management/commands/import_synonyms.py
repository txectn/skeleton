import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ...models import SynonymGroup, SynonymTerm

class Command(BaseCommand):
    help = "Import synonym groups and terms from a JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            type=str,
            help="Path to the synonyms JSON file.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = Path(options["file"])

        if not file_path.exists():
            raise CommandError(
                f"File not found: {file_path}"
            )

        if not file_path.is_file():
            raise CommandError(
                f"Path is not a file: {file_path}"
            )

        try:
            with file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except json.JSONDecodeError as exc:
            raise CommandError(
                f"Invalid JSON: {exc}"
            )

        if not isinstance(data, dict):
            raise CommandError(
                "JSON root must be an object containing "
                "synonym groups."
            )

        groups_created = 0
        groups_existing = 0
        terms_created = 0
        terms_existing = 0

        for group_name, terms in data.items():

            if not isinstance(group_name, str):
                raise CommandError(
                    "Synonym group names must be strings."
                )

            if not isinstance(terms, list):
                raise CommandError(
                    f"Terms for '{group_name}' must be a list."
                )

            group_name = group_name.strip()

            if not group_name:
                raise CommandError(
                    "Synonym group name cannot be empty."
                )

            group, created = SynonymGroup.objects.get_or_create(
                name=group_name,
                defaults={
                    "is_active": True,
                },
            )

            if created:
                groups_created += 1
            else:
                groups_existing += 1

            for term in terms:

                if not isinstance(term, str):
                    raise CommandError(
                        f"Term in '{group_name}' must be a string."
                    )

                term = term.strip().lower()

                if not term:
                    continue

                _, created = SynonymTerm.objects.get_or_create(
                    group=group,
                    term=term,
                    defaults={
                        "is_active": True,
                    },
                )

                if created:
                    terms_created += 1
                else:
                    terms_existing += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Synonym import completed successfully."
            )
        )

        self.stdout.write(
            f"Groups created: {groups_created}"
        )

        self.stdout.write(
            f"Groups already existing: {groups_existing}"
        )

        self.stdout.write(
            f"Terms created: {terms_created}"
        )

        self.stdout.write(
            f"Terms already existing: {terms_existing}"
        )