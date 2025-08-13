from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPiloteOrReadOnly(BasePermission):
    """Allow edit only to the plan pilote."""

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "pilote_id", None) == getattr(request.user, "id", None)
