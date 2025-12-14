import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from compiler.models import CodingChallenge

CSV_HEADERS = [
    "title",
    "slug",
    "difficulty",
    "description",
    "input_format",
    "output_format",
    "constraints",
    "sample_input",
    "sample_output",
    "test_input",
    "expected_output",
    "max_runtime_ms",
]
class Command(BaseCommand):
    help = "Load coding challenges from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to challenges CSV file")
        parser.add_argument("--truncate", action="store_true", help="Delete existing challenges before import")

    def handle(self, *args, **options):
        csv_path = Path(options['csv_path'])
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        if options["truncate"]:
            self.stdout.write("Deleting existing challenges...")
            CodingChallenge.objects.all().delete()

        with csv_path.open("r", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            missing = [h for h in CSV_HEADERS if h not in reader.fieldnames]
            if missing:
                raise CommandError(f"CSV missing headers: {missing}")
            created = 0
            updated = 0
            for row in reader:
                obj, is_created = CodingChallenge.objects.update_or_create(
                    slug=row.get("slug") or None,
                    defaults={
                        "title": row.get("title", "").strip(),
                        "difficulty": row.get("difficulty", "easy").strip().lower(),
                        "description": row.get("description", ""),
                        "input_format": row.get("input_format", ""),
                        "output_format": row.get("output_format", ""),
                        "constraints": row.get("constraints", ""),
                        "sample_input": row.get("sample_input", ""),
                        "sample_output": row.get("sample_output", ""),
                        "test_input": row.get("test_input", ""),
                        "expected_output": row.get("expected_output", ""),
                        "max_runtime_ms": int(row.get("max_runtime_ms") or 2000),
                    }
                )
                created += 1 if is_created else 0
                updated += 0 if is_created else 1

        self.stdout.write(self.style.SUCCESS(f"Import done. Created: {created}, Updated: {updated}"))
