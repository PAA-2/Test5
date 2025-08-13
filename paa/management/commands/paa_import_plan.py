import json
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser

from ...imports import import_plan

User = get_user_model()


class Command(BaseCommand):
    help = "Import a plan with actions from a JSON file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("file", type=str, help="Path to JSON file")
        parser.add_argument("username", type=str, help="Username of plan pilote")

    def handle(self, *args: Any, **options: Any) -> None:
        file_path: str = options["file"]
        username: str = options["username"]
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        pilote = User.objects.get(username=username)
        actions = data.get("actions", [])
        plan = import_plan(data["name"], pilote, actions)
        self.stdout.write(
            self.style.SUCCESS(
                f"Imported plan '{plan.nom}' with {plan.actions.count()} actions"
            )
        )
