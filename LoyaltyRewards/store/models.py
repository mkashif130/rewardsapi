from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    slogan = models.TextField(default='')
    is_active = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.IntegerField(default=0)
    updated_at = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name_plural = "Store"
