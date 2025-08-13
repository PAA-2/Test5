from django.contrib import admin

from .models import Action, ActionPlan, Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("nom", "pilote", "actif", "mode_stockage")
    search_fields = ("nom",)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("code", "theme", "priorite", "statut", "j_delta")
    search_fields = ("code", "theme")
    list_filter = ("statut", "priorite")
    filter_horizontal = ("responsables",)


@admin.register(ActionPlan)
class ActionPlanAdmin(admin.ModelAdmin):
    list_display = ("plan", "action", "visible")
    list_filter = ("plan", "visible")
