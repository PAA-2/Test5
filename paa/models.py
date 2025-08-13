import uuid
from datetime import date

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class StorageMode(models.TextChoices):
    EXCEL = "EXCEL", "Excel externe"
    INTERNE = "INTERNE", "Stockage interne"


class Priorite(models.TextChoices):
    BASSE = "BASSE", "Basse"
    MOYENNE = "MOYENNE", "Moyenne"
    HAUTE = "HAUTE", "Haute"
    CRITIQUE = "CRITIQUE", "Critique"


class Statut(models.TextChoices):
    EN_COURS = "EN_COURS", "En cours"
    EN_TRAITEMENT = "EN_TRAITEMENT", "En traitement"
    CLOTUREE = "CLOTUREE", "Clôturée"
    ARCHIVEE = "ARCHIVEE", "Archivée"
    REJETEE = "REJETEE", "Rejetée"


class EvaluationEfficacite(models.TextChoices):
    VIDE = "VIDE", "—"
    EFFICACE = "EFFICACE", "Efficace"
    PARTIELLE = "PARTIELLE", "Partielle"
    INEFFICACE = "INEFFICACE", "Inefficace"


class Plan(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    pilote = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="plans_pilotes"
    )
    lien_source = models.CharField(max_length=1024, null=True, blank=True)
    mode_stockage = models.CharField(
        max_length=16, choices=StorageMode.choices, default=StorageMode.EXCEL
    )
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("nom",)

    def __str__(self) -> str:
        return self.nom


class Action(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    structure = models.CharField(max_length=255, blank=True)
    theme = models.CharField(max_length=255, blank=True)
    zone = models.CharField(max_length=255, blank=True)
    ligne_source = models.CharField(max_length=255, blank=True)
    equipement = models.CharField(max_length=255, blank=True)
    anomalie = models.TextField(blank=True)
    action_a_mener = models.TextField(blank=True)
    priorite = models.CharField(
        max_length=16, choices=Priorite.choices, default=Priorite.MOYENNE
    )
    budget_dzd = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    responsables = models.ManyToManyField(
        User, related_name="actions_responsable", blank=True
    )
    delais = models.DateField(null=True, blank=True)
    date_realisation = models.DateField(null=True, blank=True)
    pdca_p = models.DateTimeField(null=True, blank=True)
    pdca_d = models.DateTimeField(null=True, blank=True)
    pdca_c = models.DateTimeField(null=True, blank=True)
    pdca_a = models.DateTimeField(null=True, blank=True)
    evaluation_delais = models.DateField(null=True, blank=True)
    evaluation_efficacite = models.CharField(
        max_length=16,
        choices=EvaluationEfficacite.choices,
        default=EvaluationEfficacite.VIDE,
    )
    commentaire = models.TextField(blank=True)
    statut = models.CharField(
        max_length=16, choices=Statut.choices, default=Statut.EN_COURS
    )
    j_delta = models.IntegerField(default=0)
    action_parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="actions_filles",
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="actions_creees",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["statut"]),
            models.Index(fields=["priorite"]),
        ]

    def __str__(self) -> str:
        return f"{self.code} — {self.theme or self.action_a_mener[:30]}"

    def recompute_j(self) -> int:
        today = date.today()
        if self.statut == Statut.CLOTUREE and self.delais and self.date_realisation:
            self.j_delta = int((self.date_realisation - self.delais).days)
        elif self.delais:
            self.j_delta = int((self.delais - today).days)
        else:
            self.j_delta = 0
        return self.j_delta

    def save(self, *args, **kwargs):
        self.recompute_j()
        super().save(*args, **kwargs)


class ActionPlan(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="actions")
    priorite_locale = models.CharField(
        max_length=16, choices=Priorite.choices, null=True, blank=True
    )
    notes = models.TextField(blank=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("action", "plan"),)
        ordering = ("-updated_at",)

    def __str__(self) -> str:
        return f"{self.plan} ↔ {self.action.code}"
