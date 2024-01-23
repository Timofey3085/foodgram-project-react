import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Unit


class Command(BaseCommand):
    help = "Импорт ингридиентов"

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            action="store",
            required=True,
            help="Путь к файлу с ингридиентами",
        )

    def handle(self, *args, **options):
        with open(options["path"], encoding="utf8") as csv_file:
            reader = list(csv.reader(csv_file))
            Unit.objects.bulk_create(
                [
                    Unit(name=unit_name)
                    for unit_name in {unit_name for _, unit_name in reader}
                ],
                ignore_conflicts=True,
            )
            unit_instances = Unit.objects.all()
            unit_name_id = {unit.name: unit for unit in unit_instances}
            Ingredient.objects.bulk_create(
                [
                    Ingredient(
                        name=ingredient_name,
                        measurement_unit=unit_name_id[unit_name],
                    )
                    for ingredient_name, unit_name in reader
                ]
            )

        self.stdout.write(
            self.style.SUCCESS("Ингридиенты успешно добавлены.")
        )
