from django.db import models
from django.utils import timezone


class SoftDeletionManager(models.Manager):
    """
    Custom manager class for soft deletion.

    Attributes:
    alive_only(bool): Used to specify whether to return all
                        objects(soft-deleted inclusive) or not.
    """

    def __init__(self, *args, **kwargs):
        """Initialize objects with a default value for `alive_only`"""
        self.alive_only = kwargs.pop('alive_only', True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        """
        Override get_queryset to return objects that have
        not been soft-deleted or all objects(soft-deleted inclusive).
        """
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        """
        Method to actually wipe objects from the database.
        """
        return self.get_queryset.hard_delete()


class SoftDeletionQuerySet(models.QuerySet):
    """
    Custom queryset for soft deletion.
    """

    def delete(self):
        """
        Soft-delete method: Updates the deleted_at field
        for 'soft-deleted' objects.
        """
        return super().update(delete_at=timezone.now())

    def hard_delete(self):
        """
        Hard-delete method: Actually wipe objects
        from the database.
        """
        return super().delete()


class softDeletionModel(models.Model):
    """
    Model class to implement soft deletion.

    Attributes:
    deleted_at: Holds date/time for soft-deleted objects.
    objects: Return objects that have not been soft-deleted.
    all_objects: Return all objects(soft-deleted inclusive)
    """
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        """
        Update time for soft-deleted objects.
        """
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """
        Wipe objects from the database.
        """
        super().delete()
