from django.db import models

from registration.models import Profile
from store.models import Store


class Public(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(default='')
    profile_image = models.TextField(default='')
    active = models.BooleanField(default=True)
    total_points = models.IntegerField(default=0)
    qr_code = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name_plural = "Public"


class PublicRedeems(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=False)
    points = models.IntegerField(default=0)
    public = models.ForeignKey(Public, on_delete=models.CASCADE, null=False)


class PublicStore(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    public = models.ForeignKey(Public, on_delete=models.CASCADE, null=True)
    points = models.IntegerField(default=0)
    created_at = models.IntegerField(default=0)