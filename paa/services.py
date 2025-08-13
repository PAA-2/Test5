from __future__ import annotations

from datetime import date
from typing import Sequence

from django.db import transaction

from .models import Action, ActionPlan, Plan, Statut


def create_plan(nom: str, pilote, **extra) -> Plan:
    """Create a new plan."""
    return Plan.objects.create(nom=nom, pilote=pilote, **extra)


def create_action(code: str, **extra) -> Action:
    """Create a new action."""
    return Action.objects.create(code=code, **extra)


def link_action_to_plan(action: Action, plan: Plan, **extra) -> ActionPlan:
    return ActionPlan.objects.create(action=action, plan=plan, **extra)


def close_action(action: Action, date_realisation: date | None = None) -> Action:
    action.statut = Statut.CLOTUREE
    if date_realisation is not None:
        action.date_realisation = date_realisation
    action.save()
    return action


def import_actions(plan: Plan, actions: Sequence[dict]) -> list[Action]:
    """Bulk create actions and link them to plan."""
    created: list[Action] = []
    with transaction.atomic():
        for data in actions:
            action = create_action(**data)
            link_action_to_plan(action, plan)
            created.append(action)
    return created
