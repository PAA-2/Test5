from __future__ import annotations

from typing import Iterable

from django.contrib.auth import get_user_model

from .models import Plan
from .services import create_action, link_action_to_plan

User = get_user_model()


def import_plan(name: str, pilote: User, actions: Iterable[dict]) -> Plan:
    """Create a plan and attach actions from iterable dictionaries."""
    plan = Plan.objects.create(nom=name, pilote=pilote)
    for data in actions:
        action = create_action(**data)
        link_action_to_plan(action, plan)
    return plan
