from django.db import models


class SoftDeleteMixin(models.Model):
    """
This class handle logical deleted for all model which is inheriting it
    """
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def logical_delete(self, using=None, keep_parents=False):
        """ change is_deleted to ture when object delete """
        self.is_deleted = True
        self.save()

    def delete(self, using=None, keep_parents=False):
        """ this method delete object in database"""
        super().delete(using=using, keep_parents=keep_parents)

    def save(self, *args, **kwargs):
        if not self.is_deleted:
            super().save(*args, **kwargs)
        else:
            super().save(using=self._state.db, force_insert=False, force_update=True)

