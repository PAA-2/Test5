import json
from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model

from paa import imports, services
from paa.models import Statut

User = get_user_model()


@pytest.mark.django_db
def test_plan_str_and_service_creation():
    pilote = User.objects.create(username="pilot")
    plan = services.create_plan("Plan A", pilote)
    assert str(plan) == "Plan A"


@pytest.mark.django_db
def test_action_recompute_j_and_close():
    action = services.create_action(
        code="A-1",
        delais=date.today() + timedelta(days=5),
    )
    # open action
    assert action.j_delta >= 0
    services.close_action(action, date_realisation=date.today())
    action.refresh_from_db()
    assert action.statut == Statut.CLOTUREE
    assert action.j_delta == (action.date_realisation - action.delais).days


@pytest.mark.django_db
def test_import_plan(tmp_path):
    pilote = User.objects.create(username="pilot")
    data = {
        "name": "Plan B",
        "actions": [
            {"code": "X1", "action_a_mener": "do"},
            {"code": "X2", "action_a_mener": "do2"},
        ],
    }
    file = tmp_path / "plan.json"
    file.write_text(json.dumps(data))
    plan = imports.import_plan(data["name"], pilote, data["actions"])
    assert plan.actions.count() == 2
